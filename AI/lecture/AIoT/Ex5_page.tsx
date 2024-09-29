import ConditionLight from 'components/ConditionLight';  // 공기 습도 상태를 표시하는 컴포넌트를 가져옵니다.
import ControlGroup from 'components/ControlGroup';  // 여러 제어 컴포넌트를 그룹화하는 컴포넌트를 가져옵니다.
import PageWrapper from 'components/internal/PageWrapper';  // 페이지의 레이아웃을 설정하는 컴포넌트를 가져옵니다.
import NumberDisplay from 'components/NumberDisplay';  // 숫자 데이터를 표시하는 컴포넌트를 가져옵니다.
import PushButton from 'components/PushButton';  // 버튼을 생성하는 컴포넌트를 가져옵니다.
import ToggleSwitch from 'components/ToggleSwitch';  // 토글 스위치를 생성하는 컴포넌트를 가져옵니다.
import React from 'react';  // React 라이브러리를 가져옵니다.

const Page: React.FC = function () {
  return (
    <PageWrapper title="IoT Web Component Example">  {/* 페이지 제목을 설정하고 레이아웃을 구성합니다. */}
      <ControlGroup label="DHT Sensor">  {/* DHT 센서 관련 제어 그룹을 생성합니다. */}
        <NumberDisplay label="Temperature" dataID="temperature" unit="℃" />  {/* 온도 데이터를 표시하는 컴포넌트입니다. */}
        <ToggleSwitch label="LED" dataID="light" />  {/* LED를 제어하는 토글 스위치입니다. */}
        <ToggleSwitch label="FAN" dataID="fan-onoff" />  {/* 팬을 제어하는 토글 스위치입니다. */}
        <ToggleSwitch label="Auto Mode" dataID="auto-mode" />  {/* 자동 모드를 제어하는 토글 스위치입니다. */}
      </ControlGroup>
      <ControlGroup label="Humidity Control">  {/* 습도 조절 관련 제어 그룹을 생성합니다. */}
        <NumberDisplay label="Humidity" dataID="humidity" unit="%" />  {/* 습도 데이터를 표시하는 컴포넌트입니다. */}
        <ConditionLight
          label="Air Humidity Condition"
          dataID="humidity"
          coloringRule={(humidity: number) => (humidity < 85 ? '#00FF00' : '#FF0000')}
        />  {/* 공기 습도 상태를 표시하고, 색상 규칙을 적용하는 컴포넌트입니다. */}
        <PushButton
          label="Pump"
          dataID="pump"
          buttonText="Pump Up"
          description="Push this button to pump water for 5 seconds"
        />  {/* 물을 펌핑하기 위한 버튼입니다. 5초 동안 펌프를 동작시킵니다. */}
      </ControlGroup>
    </PageWrapper>
  );
};

export default Page;  // Page 컴포넌트를 기본으로 내보냅니다.
