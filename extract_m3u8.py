import requests
import time

def grab(url):
    try:
        # Wait for 10 seconds before fetching the URL
        time.sleep(10)
        
        response = requests.get(url, timeout=15).text
    except requests.RequestException as e:
        return f"Error fetching URL: {e}"

    if '.m3u8' not in response:
        return 'No .m3u8 link found at the provided URL.'

    end = response.find('.m3u8') + 5
    tuner = 100
    while True:
        if 'https://' in response[end - tuner:end]:
            link = response[end - tuner:end]
            start = link.find('https://')
            end = link.find('.m3u8') + 5
            break
        else:
            tuner += 5
            if tuner > len(response):
                return 'Failed to find .m3u8 link.'

    try:
        streams = requests.get(link[start:end]).text.split('#EXT')
        hd = streams[-1].strip()
        st = hd.find('http')
        if st == -1:
            return 'No stream URL found.'
        else:
            m3u8_link = hd[st:].strip()
            with open('link.txt', 'a') as file:
                file.write(m3u8_link + '\n')
            return f"Link saved to link.txt: {m3u8_link}"
    except requests.RequestException as e:
        return f"Error fetching stream URL: {e}"

def main():
    url = "https://www.youtube.com/live/26LoMZZdSUA?si=Ru3f_9lpXCwvmcSg"  # Replace this URL with the one you want to test
    result = grab(url)
    print(result)

if __name__ == '__main__':
    main()
