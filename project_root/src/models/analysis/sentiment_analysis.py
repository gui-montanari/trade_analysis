import numpy as np
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class SentimentScore:
    overall: float  # -1.0 to 1.0
    social_media: float
    news: float
    market_data: float
    timestamp: datetime

class SentimentAnalysis:
    def __init__(self):
        self.weights = {
            'social_media': 0.3,
            'news': 0.3,
            'market_data': 0.4
        }

    def analyze_sentiment(self, market_data: Dict) -> SentimentScore:
        """Calculate overall market sentiment"""
        try:
            # Analyze different sentiment components
            social_score = self._analyze_social_sentiment(market_data)
            news_score = self._analyze_news_sentiment(market_data)
            market_score = self._analyze_market_sentiment(market_data)
            
            # Calculate weighted average
            overall_score = (
                social_score * self.weights['social_media'] +
                news_score * self.weights['news'] +
                market_score * self.weights['market_data']
            )
            
            return SentimentScore(
                overall=overall_score,
                social_media=social_score,
                news=news_score,
                market_data=market_score,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            print(f"Error in sentiment analysis: {str(e)}")
            return self._create_neutral_score()

    def _analyze_social_sentiment(self, data: Dict) -> float:
        """Analyze social media sentiment"""
        if 'social_data' not in data:
            return 0.0
            
        social_data = data['social_data']
        sentiment_indicators = [
            self._analyze_twitter_sentiment(social_data),
            self._analyze_reddit_sentiment(social_data),
            self._analyze_telegram_sentiment(social_data)
        ]
        
        return np.mean([s for s in sentiment_indicators if s is not None])

    def _analyze_news_sentiment(self, data: Dict) -> float:
        """Analyze news sentiment"""
        if 'news_data' not in data:
            return 0.0
            
        news_data = data['news_data']
        sentiment_factors = [
            self._analyze_headlines(news_data),
            self._analyze_article_content(news_data),
            self._analyze_publication_sentiment(news_data)
        ]
        
        return np.mean([s for s in sentiment_factors if s is not None])

    def _analyze_market_sentiment(self, data: Dict) -> float:
        """Analyze market-based sentiment indicators"""
        if not all(k in data for k in ['price', 'volume', 'indicators']):
            return 0.0
            
        indicators = data['indicators']
        
        # Calculate technical sentiment
        tech_sentiment = self._calculate_technical_sentiment(indicators)
        
        # Calculate market metrics sentiment
        market_sentiment = self._calculate_market_metrics_sentiment(data)
        
        return (tech_sentiment + market_sentiment) / 2

    def _calculate_technical_sentiment(self, indicators: Dict) -> float:
        """Calculate sentiment based on technical indicators"""
        sentiment_factors = []
        
        # RSI
        if 'rsi' in indicators:
            rsi = indicators['rsi'][-1]
            if rsi < 30:
                sentiment_factors.append(-0.8)
            elif rsi > 70:
                sentiment_factors.append(0.8)
            else:
                sentiment_factors.append((rsi - 50) / 50)
        
        # MACD
        if 'macd' in indicators and 'macd_signal' in indicators:
            macd_diff = indicators['macd'][-1] - indicators['macd_signal'][-1]
            sentiment_factors.append(np.tanh(macd_diff / 100))
        
        # Volume
        if 'volume_sma' in indicators:
            vol_ratio = indicators['volume'][-1] / indicators['volume_sma'][-1]
            sentiment_factors.append(np.tanh(vol_ratio - 1))
        
        return np.mean(sentiment_factors) if sentiment_factors else 0.0

    def _calculate_market_metrics_sentiment(self, data: Dict) -> float:
        """Calculate sentiment based on market metrics"""
        sentiment_factors = []
        
        # Price momentum
        if 'price' in data and len(data['price']) > 1:
            price_change = (data['price'][-1] / data['price'][-2] - 1)
            sentiment_factors.append(np.tanh(price_change * 10))
        
        # Volume profile
        if 'volume_profile' in data:
            vol_score = 1 if data['volume_profile'] == 'accumulation' else -1
            sentiment_factors.append(vol_score)
        
        # Market depth
# Market depth
        if 'market_depth' in data:
            ask_bid_ratio = data['market_depth'].get('ask_bid_ratio', 1.0)
            sentiment_factors.append(-np.tanh(ask_bid_ratio - 1))
        
        return np.mean(sentiment_factors) if sentiment_factors else 0.0

    def _analyze_twitter_sentiment(self, social_data: Dict) -> Optional[float]:
        """Analyze Twitter sentiment"""
        if 'twitter' not in social_data:
            return None

        twitter_data = social_data['twitter']
        sentiment_score = 0.0
        
        # Analyze tweet volume
        if 'volume' in twitter_data:
            volume_change = twitter_data['volume'].get('change_24h', 0)
            sentiment_score += np.tanh(volume_change / 100) * 0.3
        
        # Analyze tweet sentiment
        if 'sentiment' in twitter_data:
            positive = twitter_data['sentiment'].get('positive', 0)
            negative = twitter_data['sentiment'].get('negative', 0)
            total = positive + negative
            if total > 0:
                sentiment_score += ((positive - negative) / total) * 0.7
        
        return sentiment_score

    def _analyze_reddit_sentiment(self, social_data: Dict) -> Optional[float]:
        """Analyze Reddit sentiment"""
        if 'reddit' not in social_data:
            return None

        reddit_data = social_data['reddit']
        sentiment_score = 0.0
        
        # Analyze post volume
        if 'post_volume' in reddit_data:
            volume_change = reddit_data['post_volume'].get('change_24h', 0)
            sentiment_score += np.tanh(volume_change / 100) * 0.3
        
        # Analyze post sentiment
        if 'sentiment' in reddit_data:
            upvote_ratio = reddit_data['sentiment'].get('upvote_ratio', 0.5)
            sentiment_score += (upvote_ratio - 0.5) * 2 * 0.7
        
        return sentiment_score

    def _analyze_telegram_sentiment(self, social_data: Dict) -> Optional[float]:
        """Analyze Telegram sentiment"""
        if 'telegram' not in social_data:
            return None

        telegram_data = social_data['telegram']
        sentiment_score = 0.0
        
        # Analyze message volume
        if 'message_volume' in telegram_data:
            volume_change = telegram_data['message_volume'].get('change_24h', 0)
            sentiment_score += np.tanh(volume_change / 100) * 0.3
        
        # Analyze message sentiment
        if 'sentiment' in telegram_data:
            positive = telegram_data['sentiment'].get('positive', 0)
            negative = telegram_data['sentiment'].get('negative', 0)
            total = positive + negative
            if total > 0:
                sentiment_score += ((positive - negative) / total) * 0.7
        
        return sentiment_score

    def _analyze_headlines(self, news_data: Dict) -> Optional[float]:
        """Analyze news headlines sentiment"""
        if 'headlines' not in news_data:
            return None
            
        headlines = news_data['headlines']
        sentiment_scores = []
        
        for headline in headlines:
            # Implement headline sentiment analysis
            # This could use NLP libraries or pre-trained models
            sentiment_scores.append(self._calculate_text_sentiment(headline))
        
        return np.mean(sentiment_scores) if sentiment_scores else None

    def _analyze_article_content(self, news_data: Dict) -> Optional[float]:
        """Analyze news article content sentiment"""
        if 'articles' not in news_data:
            return None
            
        articles = news_data['articles']
        sentiment_scores = []
        
        for article in articles:
            # Implement article content sentiment analysis
            sentiment_scores.append(self._calculate_text_sentiment(article))
        
        return np.mean(sentiment_scores) if sentiment_scores else None

    def _analyze_publication_sentiment(self, news_data: Dict) -> Optional[float]:
        """Analyze publication reputation and reliability"""
        if 'sources' not in news_data:
            return None
            
        sources = news_data['sources']
        reliability_scores = []
        
        for source in sources:
            # Calculate source reliability score
            reliability_scores.append(self._calculate_source_reliability(source))
        
        return np.mean(reliability_scores) if reliability_scores else None

    def _calculate_text_sentiment(self, text: str) -> float:
        """Calculate sentiment score for text content"""
        # Placeholder for text sentiment analysis
        # In practice, this would use NLP models or sentiment analysis libraries
        return 0.0

    def _calculate_source_reliability(self, source: Dict) -> float:
        """Calculate reliability score for news source"""
        # Placeholder for source reliability calculation
        reliability = source.get('reliability_score', 0.5)
        bias = abs(source.get('bias_score', 0))
        return reliability * (1 - bias)

    def _create_neutral_score(self) -> SentimentScore:
        """Create a neutral sentiment score for error cases"""
        return SentimentScore(
            overall=0.0,
            social_media=0.0,
            news=0.0,
            market_data=0.0,
            timestamp=datetime.now()
        )