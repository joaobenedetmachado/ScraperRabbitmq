# G1 News Scraper

--- 


## install the requirements
```bash
pip install pika requests beautifulsoup4 pandas openpyxl
```

## setup the RabbitMQ
```bash
sudo apt update
sudo apt install rabbitmq-server -y
sudo systemctl enable rabbitmq-server
sudo systemctl start rabbitmq-server
sudo rabbitmq-plugins enable rabbitmq_management
```

## run the producer
```bash
python producer.py
```

## run the consumer
```bash
python consumer.py
```
## ignore the app.py!
