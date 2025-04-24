import pandas as pd
from datetime import datetime

def process_excel(file_path):
    # Load the Excel file with explicit header definition
    df = pd.read_excel(
        file_path, 
        sheet_name=0, 
        header=0
    )

    print("1. 원본 데이터의 출결구분 값들:", df['출결구분'].unique())

    # Step 1: Unmerge B, C columns (columns '번호', '성명')
    df[['번호', '성명']] = df[['번호', '성명']].ffill()

    # Step 2: 출결구분 데이터 전처리 및 필터링
    print("2-1. 변환 전 출결구분 값들:", df['출결구분'].unique())
    df['출결구분'] = df['출결구분'].astype(str).apply(
        lambda x: '질병결석' if ('질병' in x and '결석' in x) else 
                 '출석인정결석' if x.strip() == '출석인정결석' else 
                 '출석' if x.strip() == '출석' else
                 '기타결석' if x.strip() == '기타결석' else x.strip()
    )
    
    # 사유 열 전처리
    df['사유'] = df['사유'].astype(str).apply(
        lambda x: x.split('으로 인한')[0] if '으로 인한' in x else
                 x.split('로 인한')[0] if '로 인한' in x else
                 x
    )
    
    print("2-2. 변환 후 출결구분 값들:", df['출결구분'].unique())
    
    # Step 3: Filter valid data rows
    valid_types = ['출석인정결석', '질병결석', '기타결석']  # '출석'은 제외
    filtered_data = df[df['출결구분'].isin(valid_types)].copy()
    
    print("3. 필터링 후 출결구분 값들:", filtered_data['출결구분'].unique())
    print("4. 필터링 후 데이터 건수:", len(filtered_data))

    if filtered_data.empty:
        print("경고: 필터링 후 데이터가 비어있습니다!")
        return pd.DataFrame(columns=['번호', '성명', '일자', '출결구분', '사유', '결석시작일', '결석종료일', '결석일수'])

    # Step 4: Convert '일자' column to datetime format
    filtered_data['일자'] = pd.to_datetime(
        filtered_data['일자'].str.strip('.'),
        format='%Y.%m.%d',
        errors='coerce'
    )
    
    print("5. 날짜 변환 후 데이터 건수:", len(filtered_data))

    # Step 5: Add new columns
    filtered_data['결석시작일'] = None
    filtered_data['결석종료일'] = None
    filtered_data['결석일수'] = None

    # Step 6: Group by columns and process
    group_columns = ['번호', '출결구분']  # '사유' 컬럼 제외
    merged_rows = []

    # 그룹화 전 데이터 확인
    print("\n질병결석 데이터 확인:")
    sick_data = filtered_data[filtered_data['출결구분'] == '질병결석']
    print(sick_data[['번호', '출결구분', '사유', '일자']].to_string())
    
    for name, group_data in filtered_data.groupby(group_columns):
        print(f"\n6. 처리 중인 그룹: {name}")
        print(f"   - 출결구분: {name[1]}")
        print(f"   - 데이터 건수: {len(group_data)}")
        print(f"   - 날짜 데이터: {group_data['일자'].tolist()}")
        
        group_data = group_data.sort_values('일자')
        dates = group_data['일자'].dropna().tolist()
        
        if not dates:
            print(f"   - 그룹 {name}에 유효한 날짜가 없습니다")
            continue
            
        # 연속된 날짜 그룹 찾기
        current_group = []
        current_group.append(dates[0])
        
        for i in range(1, len(dates)):
            if (dates[i] - dates[i-1]).days == 1:
                current_group.append(dates[i])
            else:
                # 현재 그룹 처리
                if current_group:
                    start_date = current_group[0]
                    end_date = current_group[-1]
                    
                    base_row = group_data[group_data['일자'] == start_date].iloc[0].copy()
                    base_row['결석시작일'] = start_date.strftime('%Y.%m.%d')
                    base_row['결석종료일'] = end_date.strftime('%Y.%m.%d')
                    
                    days_diff = (end_date - start_date).days + 1
                    base_row['결석일수'] = days_diff
                    
                    if start_date != end_date:
                        base_row['일자'] = f"{start_date.strftime('%Y.%m.%d')} ~ {end_date.strftime('%Y.%m.%d')}"
                    else:
                        base_row['일자'] = start_date.strftime('%Y.%m.%d')
                    
                    # NaN 사유를 '사유입력'으로 대체
                    if pd.isna(base_row['사유']):
                        base_row['사유'] = '사유입력'
                    
                    merged_rows.append(base_row)
                
                current_group = [dates[i]]
        
        # 마지막 그룹 처리
        if current_group:
            start_date = current_group[0]
            end_date = current_group[-1]
            
            base_row = group_data[group_data['일자'] == start_date].iloc[0].copy()
            base_row['결석시작일'] = start_date.strftime('%Y.%m.%d')
            base_row['결석종료일'] = end_date.strftime('%Y.%m.%d')
            
            days_diff = (end_date - start_date).days + 1
            base_row['결석일수'] = days_diff
            
            if start_date != end_date:
                base_row['일자'] = f"{start_date.strftime('%Y.%m.%d')} ~ {end_date.strftime('%Y.%m.%d')}"
            else:
                base_row['일자'] = start_date.strftime('%Y.%m.%d')
            
            # NaN 사유를 '사유입력'으로 대체
            if pd.isna(base_row['사유']):
                base_row['사유'] = '사유입력'
            
            merged_rows.append(base_row)

    # Create final DataFrame
    columns_order = ['번호', '성명', '일자', '출결구분', '사유', '결석시작일', '결석종료일', '결석일수']
    if merged_rows:
        processed_data = pd.DataFrame(merged_rows)
        processed_data = processed_data[columns_order]
        print("7. 최종 처리된 데이터 건수:", len(processed_data))
    else:
        print("7. 처리된 데이터가 없습니다")
        processed_data = pd.DataFrame(columns=columns_order)

    return processed_data
