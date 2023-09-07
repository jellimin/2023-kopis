# 웹사이트 폴더를 가져와서 Flask APP 생성 후 실행
from website import create_app

app = create_app()

if __name__ == "__main__":
    # 디버그 모드 : 코드가 중간에 변경하고 저장할 때 자동으로 현재 서버를 재실행
    app.run('0.0.0.0', port=5000, debug=True)