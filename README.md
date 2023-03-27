# Django-channels를 이용하여 채팅 서비스 만들기
### Django-channels를 이용하여 웹소켓을 만들어보자

## Websocket
- 연결이 유지되는 동안, 양방향 통신
- 클라이언트/서버 상호 간에 즉시성이 높은 데이터 전송

## Redis 
- 서버 단에서 채팅방의 다른 유저들로의 메세지 전달자 역할. 유저로의 전달은 웹소켓을 활용.
- 레디스 특정 채널에 구독신청을 하면 구독자(Subscriber)가 됩니다. 레디스 특정 채널에 메세지를 발행(Publish)하면, 구독 중인 구독자에게 메세지가 전달 (ex.유튜브 구독)
- 레디스의 Pub/Sub는 메세지를 "전달하는" 시스템이기에 메세지를 보관하지 않음(지난 채팅 메세지 조회가 필요하다면, 메세지를 DB에 넣어두고 필요할 때 조회)
- 서버 대수를 늘려 Horizontal로 손쉬운 Scale out을 지원

## Django-channels
- ASGI기반의 라이브러로서, Http/웹소켓 프로토콜을 손쉽게 처리할 수 있도록 기능 지원, 프로세스 간 통신 가능
- 웹소켓 연결수락 및 끊기, 데이터 송,수신 기능
- Django의 기능도 이용가능
- 채널스에는 핵심개념으로서 채널,그룹이 있다. 
- 채널 
1. Consumer instance 내부에서 생성 (Consumer instance는 Redis Pub/Sub과 유저의 메시지 중개자)
2. 하나의 연결마다 Consumer 클래스의 인스턴스가 자동생성되며, 각 Consumer instance마다 고유한 채널명을 가짐
3. 그 채널을 통해 Consumer instance는 채널 레이어(Redis)와 통신
- 그룹 : 여러 Consumer Instance를 묶는 논리적인 묶음

## Redis, Channels(채널스) 간단한 구현 원리
