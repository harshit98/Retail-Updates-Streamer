# Retail Updates Streamer

EuroPython 2021 - High Performance Data Processing using Python, Kafka and Elasticsearch.

## Prerequisites

- Python >= 3.6
- FastAPI
- Kafka
- Elasticsearch

## Workflow Architecture

<p align="center" width="100%">
    <img alt="workflow-architecture" src="assets/producer-consumer.png"> 
</p>

## Setup

1. Make sure Python >= 3.6 is installed on your local machine and create a virtual environment.

   ```bash
   python3 -m venv realtime-updates-service
   ```

2. Activate your virtual environment.

   ```bash
   source realtime-updates-service/bin/activate
   ```

3. Install application packages.

   ```bash
   pip install -r requirements.txt
   ```

4. Add your producer-consumer related config in a `.env` file.

## Scripts

Scripts can be used to create your own dummy data and play with producer-consumer code.

Any script can be run using:

```
python3 <FILE_NAME>.py
```

## Author

👤 Harshit Prasad

Twitter: [@HarshitPrasad8](https://twitter.com/HarshitPrasad8)
Github: [@harshit98](https://github.com/harshit98)
Website: [harshitprasad.com](http://harshitprasad.com)
LinkedIn: [harshit-prasad](https://www.linkedin.com/in/harshit-prasad/)

## 🤝 Contributing

Contributions, issues and feature requests are welcome!

## Show your support

Give a ⭐️ if you think this project is awesome!

## 📝 License

Copyright © 2020 [Harshit Prasad](https://github.com/harshit98).
This project is [Apache License](https://github.com/harshit98/personalized-search/blob/master/LICENSE) licensed.
