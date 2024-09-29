#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <AsyncTimer.h>
#include <DHT11.h>
#include <Sprigatito.h>
#include <Wire.h>
#include <CytronMotorDriver.h>

/* Pin Mapping */
#define DHT_PIN 31      // DHT11 센서가 연결된 핀 번호입니다.
#define PWM1A_PIN 5     // 팬 모터의 PWM 제어 핀 1입니다.
#define PWM1B_PIN 6     // 팬 모터의 PWM 제어 핀 2입니다.

// NOTE: For OLED, we're going to use default pins for I2C communication.

/* Instantiation */
// OLED 디스플레이 객체를 생성합니다. (128x64 해상도, I2C 통신)
Adafruit_SSD1306 oled(128, 64, &Wire, -1);
// 비동기 타이머 객체를 생성합니다.
AsyncTimer timer;
// DHT11 온습도 센서 객체를 생성합니다.
DHT11 dht;
// Cytron 모터 드라이버 객체를 생성합니다. (PWM 모드, 제어 핀 설정)
CytronMD fan(PWM_PWM, PWM1A_PIN, PWM1B_PIN);

char tempStr[32];       // 온도를 저장할 문자열 버퍼입니다.
char humidity[32];      // 습도를 저장할 문자열 버퍼입니다.
char fanStatusStr[32];  // 팬 상태를 저장할 문자열 버퍼입니다.
uint8_t fanSpeed = 0;   // 팬 속도 값을 저장할 변수입니다.

/* Setup */
void setup() {
  Serial.begin(115200); // 시리얼 통신을 115200bps로 시작합니다. 

  if(!oled.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { // OLED 디스플레이를 초기화합니다. I2C 주소는 0x3C입니다.
    Serial.println(F("SSD1306 allocation failed")); // 초기화에 실패하면 메시지를 출력하고 프로그램을 중지합니다.
    for(;;); // stop here
  }
  oled.display(); // 초기화된 디스플레이 내용을 화면에 표시합니다.
  oled.setTextSize(1); // One character = 6x8
  oled.setTextColor(SSD1306_WHITE); // 텍스트 색상을 흰색으로 설정합니다.
  oled.cp437(true); // CP437 문자 세트를 사용하도록 설정합니다.

  // OLED 화면에 그림 및 텍스트를 주기적으로 표시하는 타이머를 설정합니다.
  timer.setInterval([]() {
    oled.clearDisplay();  // 화면을 지웁니다.
    oled.drawBitmap(0, 0, Sprigatito, 64, 64, 1);  // 화면에 Sprigatito 이미지를 그립니다.
    oled.setCursor(62, 0);   // 텍스트 커서를 설정합니다. (x: 62, y: 0)
    oled.write("[Temp&Humi]");  // "[Temp&Humi]" 텍스트를 표시합니다.
    oled.setCursor(68, 10);  // 텍스트 커서를 설정합니다. (x: 68, y: 10)
    oled.write(tempStr);     // 현재 온도를 표시합니다.
    oled.setCursor(68, 20);  // 텍스트 커서를 설정합니다. (x: 68, y: 20)
    oled.write(humidity);    // 현재 습도를 표시합니다.
    oled.setCursor(68, 30);  // 텍스트 커서를 설정합니다. (x: 68, y: 30)
    oled.write(fanStatusStr);  // 팬 상태를 표시합니다.
    
    oled.display();  // 화면에 그려진 내용을 실제 디스플레이에 출력합니다.
  }, 1000);  // 1초(1000ms)마다 반복 실행합니다.

  // DHT 센서에서 데이터를 읽어와서 팬 속도를 제어하는 타이머를 설정합니다.
  timer.setInterval([]() {
    dht.read(DHT_PIN);  // DHT 센서로부터 데이터를 읽어옵니다.
    sprintf(tempStr, "T : %d C", dht.temperature);  // 온도를 문자열로 변환하여 저장합니다.
    sprintf(humidity, "H : %d %%", dht.humidity);   // 습도를 문자열로 변환하여 저장합니다.

    // 팬 속도 제어 논리입니다.
    if (dht.temperature >= 30) {
      fanSpeed = 100;  // 온도가 30도 이상이면 팬을 최대 속도로 설정합니다.
    } else if (dht.temperature < 25) {
      fanSpeed = 0;    // 온도가 25도 이하이면 팬을 끕니다.
    } else {
      fanSpeed = 65;   // 온도가 25도와 30도 사이이면 팬을 중간 속도로 설정합니다.
    }

    fan.setSpeed(fanSpeed);  // 계산된 팬 속도를 적용합니다.
    sprintf(fanStatusStr, "Fan: %d %%", fanSpeed);  // 팬 속도를 문자열로 변환하여 저장합니다.
  }, 750); // 750ms마다 반복 실행합니다.
}

/* loop */
void loop() {
  timer.handle();  // 설정된 타이머 이벤트를 처리합니다.
}
