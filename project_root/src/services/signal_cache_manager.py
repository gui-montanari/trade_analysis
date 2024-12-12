from typing import Dict, Optional
from datetime import datetime
import json
from pathlib import Path

class SignalCacheManager:
    def __init__(self):
        self.cache_file = Path("cache/trading_signals.json")
        self.cache_file.parent.mkdir(exist_ok=True)
        self._load_cache()

    def _load_cache(self):
        """Load cached signals"""
        try:
            if self.cache_file.exists():
                with open(self.cache_file, 'r') as f:
                    self.cached_signals = json.load(f)
            else:
                self.cached_signals = {}
        except Exception as e:
            print(f"Error loading signal cache: {e}")
            self.cached_signals = {}

    def _save_cache(self):
        """Save signals to cache"""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.cached_signals, f, indent=2)
        except Exception as e:
            print(f"Error saving signal cache: {e}")

    def get_first_signal(self, trading_type: str) -> Optional[Dict]:
        """Get first signal for trading type"""
        return self.cached_signals.get(trading_type)

    def update_signal(self, trading_type: str, signal: Dict, current_direction: str):
        """Update signal if direction changed"""
        cached_signal = self.cached_signals.get(trading_type)
        
        if not cached_signal or cached_signal.get('direction') != current_direction:
            # New signal with direction change
            self.cached_signals[trading_type] = {
                'direction': current_direction,
                'entry_price': signal.get('entry_price', 0),
                'take_profit': signal.get('take_profit', 0),
                'stop_loss': signal.get('stop_loss', 0),
                'confidence': signal.get('confidence', 0),
                'timestamp': datetime.now().isoformat()
            }
            self._save_cache()

    def clear_cache(self):
        """Clear all cached signals"""
        self.cached_signals = {}
        self._save_cache()