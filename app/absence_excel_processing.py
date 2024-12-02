import pandas as pd
from datetime import datetime

def process_excel(file_path):
    # Load the Excel file with explicit header definition
    df = pd.read_excel(
        file_path, 
        sheet_name=0, 
        header=0  # 첫 번째 행을 헤더로 설정
    )

    # Step 1: Unmerge B, C columns (columns '번호', '성명')
    df[['번호', '성명']] = df[['번호', '성명']].ffill()

    # Step 2: Filter valid data rows
    valid_types = ['출석인정결석', '질병결석', '기타결석']
    filtered_data = df[df['출결구분'].isin(valid_types)].copy()

    # Step 3: Convert '일자' column to datetime format
    filtered_data['일자'] = pd.to_datetime(
        filtered_data['일자'].str.strip('.'),  # Trailing '.' 제거
        format='%Y.%m.%d',  # 예상되는 날짜 형식
        errors='coerce'  # 변환 실패 시 NaT로 처리
    )

    # Step 4: Add new columns
    filtered_data['결석시작일'] = None
    filtered_data['결석종료일'] = None
    filtered_data['결석일수'] = None  # 새로운 열 추가

    # Step 5: Group by '출결구분', '사유', and '번호' and find continuous dates
    group_columns = ['번호', '출결구분', '사유']
    merged_rows = []

    for _, group_data in filtered_data.groupby(group_columns):
        # 날짜로 정렬
        group_data = group_data.sort_values('일자')
        dates = group_data['일자'].dropna().tolist()
        
        if not dates:  # 유효한 날짜가 없는 경우 스킵
            continue
            
        # 연속된 날짜 그룹 찾기
        current_group = []
        current_group.append(dates[0])
        
        for i in range(1, len(dates)):
            # 이전 날짜와 현재 날짜의 차이가 1일인 경우
            if (dates[i] - dates[i-1]).days == 1:
                current_group.append(dates[i])
            else:
                # 현재 그룹 처리
                if len(current_group) >= 1:  # 1일 이상인 경우도 포함
                    start_date = current_group[0]
                    end_date = current_group[-1]
                    
                    # 해당 기간의 첫 번째 행 데이터 가져오기
                    base_row = group_data[group_data['일자'] == start_date].iloc[0].copy()
                    
                    # 날짜 정보 업데이트
                    base_row['결석시작일'] = start_date.strftime('%Y.%m.%d')
                    base_row['결석종료일'] = end_date.strftime('%Y.%m.%d')
                    
                    # 결석일수 계산 (종료일 - 시작일 + 1)
                    days_diff = (end_date - start_date).days + 1
                    base_row['결석일수'] = days_diff
                    
                    # 일자 열에 기간 표시
                    if start_date != end_date:
                        base_row['일자'] = f"{start_date.strftime('%Y.%m.%d')} ~ {end_date.strftime('%Y.%m.%d')}"
                    else:
                        base_row['일자'] = start_date.strftime('%Y.%m.%d')
                    
                    merged_rows.append(base_row)
                
                # 새로운 그룹 시작
                current_group = [dates[i]]
        
        # 마지막 그룹 처리
        if current_group:
            start_date = current_group[0]
            end_date = current_group[-1]
            
            base_row = group_data[group_data['일자'] == start_date].iloc[0].copy()
            base_row['결석시작일'] = start_date.strftime('%Y.%m.%d')
            base_row['결석종료일'] = end_date.strftime('%Y.%m.%d')
            
            # 결석일수 계산
            days_diff = (end_date - start_date).days + 1
            base_row['결석일수'] = days_diff
            
            if start_date != end_date:
                base_row['일자'] = f"{start_date.strftime('%Y.%m.%d')} ~ {end_date.strftime('%Y.%m.%d')}"
            else:
                base_row['일자'] = start_date.strftime('%Y.%m.%d')
            
            merged_rows.append(base_row)

    # Create final DataFrame from merged rows
    if merged_rows:
        processed_data = pd.DataFrame(merged_rows)
        # Reorder columns if needed
        columns_order = ['번호', '성명', '일자', '출결구분', '사유', '결석시작일', '결석종료일', '결석일수']
        processed_data = processed_data[columns_order]
    else:
        processed_data = pd.DataFrame(columns=columns_order)

    return processed_data


