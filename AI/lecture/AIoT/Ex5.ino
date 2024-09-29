#include <Adafruit_GFX.h>           
#include <Adafruit_SSD1306.h>       
#include <CytronMotorDriver.h>      
#include <Sprigatito.h>              
#include <Wire.h>
#include <AsyncTimer.h>
#include <DHT11.h>                  
#include <VegemiteSandwich.h>       

#define DHT_PIN 31      // DHT11 센서가 연결된 핀 번호입니다.
#define PUMP_PIN 4      // 펌프 제어를 위한 핀 번호입니다.
#define PWM1A_PIN 5     // 모터 드라이버의 PWM 제어 핀 1입니다.
#define PWM1B_PIN 6     // 모터 드라이버의 PWM 제어 핀 2입니다.
#define LED1_PIN 8      // LED1 제어를 위한 핀 번호입니다.
#define LED2_PIN 9      // LED2 제어를 위한 핀 번호입니다.

// 주요 장치 인스턴스 생성
Adafruit_SSD1306 oled(128, 64, &Wire, -1);     // OLED 디스플레이 객체입니다. (128x64 해상도, I2C 통신)
CytronMD fan(PWM_PWM, PWM1A_PIN, PWM1B_PIN);   // Cytron 모터 드라이버 객체입니다.
AsyncTimer timer;                              // 비동기 타이머 객체입니다.
VegemiteSandwich vs(&Serial2);                 // VegemiteSandwich 객체입니다.
DHT11 dht;                                     // DHT11 온습도 센서 객체입니다.

/* Setup */
void setup() {
    Serial.begin(115200);  // 시리얼 통신을 115200bps로 초기화합니다.
    
    // OLED 디스플레이를 초기화합니다. I2C 주소는 0x3C입니다.
    if(!oled.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {      
        Serial.println(F("SSD1306 allocation failed"));  // OLED 초기화 실패 시 메시지를 출력합니다.
        for(;;); // 여기서 프로그램을 멈춥니다.
    }
    oled.display();  // 초기화된 디스플레이 내용을 화면에 표시합니다.
    oled.setTextSize(1);  // 텍스트 크기를 1로 설정합니다. (한 글자 = 6x8 크기)
    oled.setTextColor(SSD1306_WHITE);  // 텍스트 색상을 흰색으로 설정합니다.
    oled.cp437(true);  // CP437 문자 세트를 사용하도록 설정합니다.
    
    // 펌프와 LED 핀을 출력 모드로 설정합니다.
    pinMode(PUMP_PIN, OUTPUT);  
    pinMode(LED1_PIN, OUTPUT);  
    pinMode(LED2_PIN, OUTPUT);  

    // ESP-01 모듈과의 통신을 설정합니다.
    vs.waitForESP01();  // ESP-01 모듈이 준비될 때까지 대기합니다.
    vs.connectAP("A_2.4GHz", "piai4101");  // 지정된 SSID와 비밀번호로 Wi-Fi에 연결합니다.
    vs.connectTCP("141.223.140.31", 3010);  // 지정된 IP 주소와 포트로 TCP 연결을 설정합니다.
    vs.registerHandler(&timer);  // 타이머 핸들러를 등록하여 주기적으로 작업을 수행합니다.

    // OLED 디스플레이에 온습도와 Auto Mode 상태를 표시하는 타이머를 설정합니다.
    timer.setInterval([]() {
        char tempStr[10];  // 온도를 저장할 문자열 버퍼입니다.
        char humidityStr[10];  // 습도를 저장할 문자열 버퍼입니다.
        char autoModeStr[10];  // Auto Mode 상태를 저장할 문자열 버퍼입니다.
      
        // DHT11 센서에서 온습도를 읽어와 문자열로 변환합니다.
        snprintf(tempStr, sizeof(tempStr), "%dC", dht.temperature);
        snprintf(humidityStr, sizeof(humidityStr), "%d%%", dht.humidity);
        snprintf(autoModeStr, sizeof(autoModeStr), "Auto:%s", vs.get("auto-mode") > 0 ? "ON" : "OFF");
      
        oled.clearDisplay();  // 화면을 지웁니다.
        oled.drawBitmap(0, 0, Sprigatito, 64, 64, 1);  // OLED 화면에 Sprigatito 이미지를 그립니다.
        oled.setCursor(68, 0); // 텍스트 커서를 설정합니다. (x: 68, y: 0)
        oled.print("[Temp&Humi]");  // "[Temp&Humi]" 텍스트를 표시합니다.
        oled.setCursor(68, 10); // 텍스트 커서를 설정합니다. (x: 68, y: 10)
        oled.print(tempStr);  // 온도를 표시합니다.
        oled.setCursor(68, 20); // 텍스트 커서를 설정합니다. (x: 68, y: 20)
        oled.print(humidityStr);  // 습도를 표시합니다.
        oled.setCursor(68, 30);  // 텍스트 커서를 설정합니다. (x: 68, y: 30)
        oled.print(autoModeStr);  // Auto Mode 상태를 표시합니다.
      
        if (dht.humidity >= 65) {  // 습도가 65% 이상일 때 "Nya~~" 메시지를 표시합니다.
            oled.setCursor(70, 40);
            oled.print("Nya~~");
        }
        oled.display();  // 그린 내용을 OLED 화면에 표시합니다.
    }, 1000);  // 1초(1000ms)마다 반복 실행합니다.

    // 주기적으로 DHT11 센서로부터 온습도 정보를 읽어와 ESP-01 모듈을 이용해 전송합니다.
    timer.setInterval([&]() {                      
        dht.read(DHT_PIN);  // DHT11 센서에서 온습도 값을 읽어옵니다.
        vs.put("temperature", dht.temperature);  // 읽어온 온도 데이터를 서버로 전송합니다.
        vs.put("humidity", dht.humidity);  // 읽어온 습도 데이터를 서버로 전송합니다.
    }, 1000);  // 1초마다 실행합니다.

    // Auto Mode 동작 설정입니다.
    // Auto Mode가 활성화되면 습도와 온도에 따라 펌프와 팬이 자동으로 동작합니다.
    // Auto Mode가 비활성화되면 수동 스위치를 통해 펌프와 팬을 제어합니다.
    timer.setInterval([&]() {
        if (vs.get("auto-mode") > 0) {  // Auto Mode가 켜져 있는 경우
            if (dht.humidity < 50) {  // 습도가 50%보다 낮으면 펌프를 끕니다.
                digitalWrite(PUMP_PIN, LOW);    
            } else {
                digitalWrite(PUMP_PIN, HIGH);  // 습도가 50%보다 높으면 펌프를 켭니다.
            }

            // 온도가 27도보다 높으면 팬을 켭니다.
            if (dht.temperature > 27) {
                fan.setSpeed(255);
            } else {
                fan.setSpeed(0);
            }
        } else {
            // Auto Mode가 꺼져 있을 때는 팬과 펌프를 수동으로 제어합니다.
            digitalWrite(PUMP_PIN, vs.getAndClear("pump") ? LOW : HIGH);
            fan.setSpeed(vs.get("fan-onoff") > 0 ? 255 : 0);
        }
    }, 1000);  // 1초마다 실행합니다.

    // 웹에서 펌프 동작 스위치에 따라 펌프를 제어하는 코드입니다.
    // 수동 모드일 때만 동작합니다 (auto-mode == 0).
    timer.setInterval([&]() {
        if(vs.get("auto-mode") == 0) {
            digitalWrite(PUMP_PIN, vs.getAndClear("pump") ? LOW : HIGH);
        }
    }, 5000);  // 5초마다 실행합니다.

    // 웹에서 팬 동작 스위치에 따라 팬을 제어하는 코드입니다.
    // 수동 모드일 때만 동작합니다 (auto-mode == 0).
    timer.setInterval([&]() {
        if(vs.get("auto-mode") == 0) {
            fan.setSpeed(vs.get("fan-onoff") > 0 ? 255 : 0);
        }
    }, 1000);  // 1초마다 실행합니다.


    // 웹에서 빛 스위치와 예측 온도값에 따라 LED를 제어하는 코드입니다.
    // LED1은 예측 기온의 1의 자리수에 따라, LED2는 10의 자리수에 따라 밝기가 조절됩니다.
    // 수동 모드일 때만 동작합니다 (auto-mode == 0).
    timer.setInterval([&]() {
        if(vs.get("auto-mode") == 0) {  // Auto Mode가 꺼져 있을 때만 동작합니다.
            auto futureTemp = vs.infer("temperature");  // 미래의 온도를 예측합니다.
            if (vs.get("light") > 0) {  // 빛 스위치가 켜져 있을 때
                // LED1의 밝기를 예측 온도의 1의 자리수에 따라 설정합니다.
                analogWrite(LED1_PIN, min(pow(int(futureTemp) % 10, 3), 255));
                // LED2의 밝기를 예측 온도의 10의 자리수에 따라 설정합니다.
                analogWrite(LED2_PIN, min(pow(int(futureTemp) / 10, 3), 255));
            } else {  // 빛 스위치가 꺼져 있을 때
                analogWrite(LED1_PIN, 0);  // LED1을 끕니다.
                analogWrite(LED2_PIN, 0);  // LED2를 끕니다.
            }
        }
    }, 2500);  // 2.5초마다 실행합니다.

}

/* Loop */
void loop() {
    timer.handle();  // 설정된 타이머 이벤트를 처리합니다.
}