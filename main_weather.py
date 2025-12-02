import requests
import json

def main():
    # -----------------------------------------------------
    # ★ 여기에 본인의 API 키를 입력하세요 (Decoding된 키) ★
    my_key = "4f01481ceb3f202a3773f3520571148fb81644f5caffcf49c3a540138bc34030"
    # -----------------------------------------------------

    print("=== 기상청 단기예보 조회 정보를 입력해주세요 ===")
    
    # 1. 사용자에게 직접 값을 입력받는 부분 (input 함수 사용)
    # 프로그램이 실행되면 여기서 입력을 기다립니다.
    base_date = input("1. 예보 날짜를 입력하세요 (형식: YYYYMMDD, 예: 20251202): ")
    base_time = input("2. 발표 시각을 입력하세요 (형식: 0200, 0500, 0800...): ")
    nx = input("3. 예보지점 X 좌표를 입력하세요 (예: 65): ")
    ny = input("4. 예보지점 Y 좌표를 입력하세요 (예: 114): ")

    # 2. 입력된 정보 확인 출력 (요청하신 스타일)
    print("\n")
    print(f"● 예보 날짜(YYYYMMDD): {base_date}")
    print(f"  발표 시각(0200/0500/0800/1100/1400/1700/2000/2300): {base_time}")
    print(f"  예보지점 X 좌표(nx): {nx}")
    print(f"  예보지점 Y 좌표(ny): {ny}")
    print("\n")
    print("=" * 30)
    print(f"📌 단기예보 ({base_date} 발표 {base_time})")
    print("=" * 30)

    # [cite_start]3. API 요청 설정 [cite: 44-56]
    url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
    params = {
        'serviceKey': my_key,
        'pageNo': '1',
        'numOfRows': '1000',
        'dataType': 'JSON',
        'base_date': base_date,
        'base_time': base_time,
        'nx': nx,
        'ny': ny
    }
    
    try:
        response = requests.get(url, params=params)
        res_json = response.json()
        
        # 응답 확인
        if res_json['response']['header']['resultCode'] != '00':
            print("❌ 에러 발생:", res_json['response']['header']['resultMsg'])
            return

        items = res_json['response']['body']['items']['item']
        
        # 4. 데이터 가공
        forecast_data = {}
        for item in items:
            key = f"{item['fcstDate']} {item['fcstTime']}"
            if key not in forecast_data:
                forecast_data[key] = {}
            forecast_data[key][item['category']] = item['fcstValue']

        # [cite_start]5. 결과 출력 (코드값 매핑) [cite: 71-76]
        count = 0
        for key, data in forecast_data.items():
            if count >= 5: break # 5개 시간대만 출력
            
            time_str = f"{key[9:11]}시{key[11:]}분"
            
            temp = data.get('TMP', '-')       # 기온
            pop = data.get('POP', '-')        # 강수확률
            wsd = data.get('WSD', '-')        # 풍속
            reh = data.get('REH', '-')        # 습도
            
            # 하늘상태 (SKY)
            sky_code = data.get('SKY', '0')
            sky_str = ""
            if sky_code == '1': sky_str = "맑음"
            elif sky_code == '3': sky_str = "구름많음"
            elif sky_code == '4': sky_str = "흐림"
            
            # 강수형태 (PTY)
            pty_code = data.get('PTY', '0')
            pty_str = "없음"
            if pty_code == '1': pty_str = "비"
            elif pty_code == '2': pty_str = "비/눈"
            elif pty_code == '3': pty_str = "눈"
            elif pty_code == '4': pty_str = "소나기"
            
            print(f"⏰ 예보시각: {time_str}")
            print(f"  🌡️ 기온: {temp} °C")
            print(f"  💧 강수확률: {pop} %")
            print(f"  ☔ 강수형태: {pty_str}")
            print(f"  ☁️ 하늘상태: {sky_str}")
            print(f"  🍃 풍속: {wsd} m/s")
            print(f"  💦 습도: {reh} %")
            print("-" * 30)
            
            count += 1

    except Exception as e:
        print(f"오류가 발생했습니다: {e}")
        print("입력한 날짜나 시간 형식이 맞는지 확인해주세요.")

if __name__ == "__main__":
    main()