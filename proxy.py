import requests
from stem import Signal
from stem.control import Controller


def get_tor_session():
    # инициализировать сеанс запросов
    session = requests.Session()
    # установка прокси для http и https на localhost: 9050
    # для этого требуется запущенная служба Tor на вашем компьютере и прослушивание порта 9050 (по умолчанию)
    session.proxies = {
        "http": "socks5://localhost:9050",
        "https": "socks5://localhost:9050",
    }
    return session


def renew_connection():
    with Controller.from_port(port=9151) as c:
        c.authenticate()
        # отправить сигнал NEWNYM для установления нового чистого соединения через сеть Tor
        c.signal(Signal.NEWNYM)


if __name__ == "__main__":
    s = get_tor_session()
    ip = s.get("http://icanhazip.com").text
    print("IP:", ip)
    renew_connection()
    s = get_tor_session()
    ip = s.get("http://icanhazip.com").text
    print("IP:", ip)
