import subprocess
import re
import hashlib
import threading
import time

class WiFiScanner:
    def __init__(self):
        self.networks = []
        self._lock = threading.Lock()
        self._running = False
        self._thread = None
        
    def start_scanning(self, interval=5):
        self._running = True
        self._thread = threading.Thread(target=self._scan_loop, args=(interval,), daemon=True)
        self._thread.start()
        
    def stop_scanning(self):
        self._running = False
        if self._thread:
            self._thread.join()
            
    def get_networks(self):
        with self._lock:
            # return a copy
            return list(self.networks)
            
    def _scan_loop(self, interval):
        # Do an initial scan before looping
        new_networks = self.scan()
        with self._lock:
            self.networks = new_networks
            
        while self._running:
            time.sleep(interval)
            if not self._running:
                break
            new_networks = self.scan()
            with self._lock:
                self.networks = new_networks
            
    def scan(self):
        try:
            # We use netsh wlan show networks mode=bssid on Windows
            # It provides SSID, BSSID, Signal, etc.
            result = subprocess.run(['netsh', 'wlan', 'show', 'networks', 'mode=bssid'], capture_output=True, text=True, errors='replace')
            output = result.stdout
            return self._parse_netsh_output(output)
        except Exception as e:
            print(f"Error scanning WiFi: {e}")
            return []
            
    def _parse_netsh_output(self, output):
        networks = []
        lines = output.split('\n')
        current_ssid = ""
        
        # Regex patterns
        ssid_pattern = re.compile(r"^SSID\s+\d+\s+:\s+(.*)$")
        bssid_pattern = re.compile(r"^\s+BSSID\s+\d+\s+:\s+([a-fA-F0-9:]+)$")
        signal_pattern = re.compile(r"^\s+Signal\s+:\s+(\d+)%$")
        
        current_network = None
        
        for line in lines:
            line = line.rstrip()
            
            # Check SSID
            match = ssid_pattern.match(line)
            if match:
                current_ssid = match.group(1).strip()
                continue
                
            # Check BSSID
            match = bssid_pattern.match(line)
            if match:
                bssid = match.group(1).strip()
                current_network = {
                    "ssid": current_ssid,
                    "bssid": bssid,
                    "signal": 0,
                    # Generate a stable artificial angle for this MAC address
                    # The angle is 0 to 360 degrees
                    "angle": int(hashlib.md5(bssid.encode()).hexdigest(), 16) % 360,
                    "distance": 0.0,
                    "last_seen": time.time()
                }
                networks.append(current_network)
                continue
                
            # Check Signal
            if current_network:
                match = signal_pattern.match(line)
                if match:
                    signal = int(match.group(1))
                    current_network["signal"] = signal
                    # Convert signal % to an approximate distance factor (0-100% -> 300 to 0)
                    # For a radar radius of 300, 100% signal could be distance 20, 10% could be distance 290
                    dist = 300 - (signal * 2.8)
                    current_network["distance"] = max(10, min(300, dist))
                    
                    # After getting signal, this network entry is complete enough for our needs.
                    current_network = None
                    continue
                    
        return networks
        
def main():
    scanner = WiFiScanner()
    nets = scanner.scan()
    print(f"Found {len(nets)} networks.")
    for n in nets:
        print(f"SSID: {n['ssid']:<20} | BSSID: {n['bssid']} | Signal: {n['signal']}% | Distance: {n['distance']:.1f} | Angle: {n['angle']}")


if __name__ == "__main__":
    main()
