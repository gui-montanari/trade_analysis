import numpy as np
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class Pattern:
    name: str
    confidence: float
    type: str  # 'bullish' or 'bearish'
    start_idx: int
    end_idx: int

class PatternRecognition:
    def __init__(self):
        self.min_pattern_confidence = 65.0

    def identify_patterns(self, prices: List[float], highs: List[float], 
                        lows: List[float]) -> List[Pattern]:
        patterns = []
        
        # Check candlestick patterns
        patterns.extend(self.identify_candlestick_patterns(prices))
        
        # Check chart patterns
        patterns.extend(self.identify_chart_patterns(prices, highs, lows))
        
        return [p for p in patterns if p.confidence >= self.min_pattern_confidence]

    def identify_candlestick_patterns(self, prices: List[float]) -> List[Pattern]:
        """Identify candlestick patterns in price data"""
        patterns = []
        
        # Check for doji
        doji = self._find_doji(prices)
        if doji:
            patterns.extend(doji)
        
        # Check for hammer/hanging man
        hammer = self._find_hammer(prices)
        if hammer:
            patterns.extend(hammer)
        
        # Check for engulfing patterns
        engulfing = self._find_engulfing(prices)
        if engulfing:
            patterns.extend(engulfing)
        
        return patterns

    def identify_chart_patterns(self, prices: List[float], highs: List[float], 
                              lows: List[float]) -> List[Pattern]:
        """Identify chart patterns in price data"""
        patterns = []
        
        # Head and shoulders
        head_shoulders = self._find_head_shoulders(prices, highs, lows)
        if head_shoulders:
            patterns.extend(head_shoulders)
        
        # Double top/bottom
        double_patterns = self._find_double_patterns(prices, highs, lows)
        if double_patterns:
            patterns.extend(double_patterns)
        
        # Triangle patterns
        triangles = self._find_triangles(prices, highs, lows)
        if triangles:
            patterns.extend(triangles)
        
        return patterns

    def _find_doji(self, prices: List[float]) -> Optional[List[Pattern]]:
        """Identify doji candlestick patterns"""
        patterns = []
        window = 5
        
        for i in range(window, len(prices)):
            if abs(prices[i] - prices[i-1]) <= 0.1 * prices[i]:
                confidence = self._calculate_pattern_confidence(prices, slice(i-window, i))
                patterns.append(Pattern(
                    name='Doji',
                    confidence=confidence,
                    type='neutral',
                    start_idx=i-1,
                    end_idx=i
                ))
                
        return patterns if patterns else None

    def _find_hammer(self, prices: List[float]) -> Optional[List[Pattern]]:
        """Identify hammer and shooting star patterns"""
        patterns = []
        window = 5
        
        for i in range(window, len(prices)):
            pattern = self._check_hammer_pattern(prices[i-window:i+1])
            if pattern:
                patterns.append(pattern)
                
        return patterns if patterns else None

    def _find_engulfing(self, prices: List[float]) -> Optional[List[Pattern]]:
        """Identify bullish and bearish engulfing patterns"""
        patterns = []
        window = 5
        
        for i in range(window, len(prices)-1):
            pattern = self._check_engulfing_pattern(prices[i-1:i+1])
            if pattern:
                patterns.append(pattern)
                
        return patterns if patterns else None

    def _find_head_shoulders(self, prices: List[float], highs: List[float], 
                           lows: List[float]) -> Optional[List[Pattern]]:
        """Identify head and shoulders patterns"""
        patterns = []
        window = 20
        
        for i in range(window, len(prices)-window):
            pattern = self._check_head_shoulders_pattern(
                prices[i-window:i+window],
                highs[i-window:i+window],
                lows[i-window:i+window]
            )
            if pattern:
                patterns.append(pattern)
                
        return patterns if patterns else None

    def _calculate_pattern_confidence(self, prices: List[float], 
                                   period: slice) -> float:
        """Calculate confidence score for pattern"""
        # Implement confidence calculation based on:
        # - Pattern clarity
        # - Volume confirmation
        # - Trend context
        # - Historical success rate
        return 75.0  # Placeholder