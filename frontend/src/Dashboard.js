import React, { useState, useEffect, useRef } from 'react';
import './Dashboard.css';

const Dashboard = () => {
  const [alerts, setAlerts] = useState([]);
  const [stats, setStats] = useState({ 
    total_alerts: 0, 
    by_severity: { HIGH: 0, MEDIUM: 0, LOW: 0 }, 
    threat_distribution: [],
    blocked_ips: 0,
    active_connections: 0
  });
  const [blockedIPs, setBlockedIPs] = useState([]);
  const [systemStatus, setSystemStatus] = useState({});
  const [wsConnected, setWsConnected] = useState(false);
  const [currentTime, setCurrentTime] = useState(new Date());
  const wsRef = useRef(null);
  const audioContextRef = useRef(null);

  // Update clock every second
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  // WebSocket Connection
  useEffect(() => {
    connectWebSocket();
    fetchInitialData();

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  const connectWebSocket = () => {
    const ws = new WebSocket('ws://localhost:8000/ws');
    wsRef.current = ws;

    ws.onopen = () => {
      console.log('✅ WebSocket Connected');
      setWsConnected(true);
    };

    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      
      if (message.type === 'alert') {
        // Add new alert to the top with animation
        setAlerts(prev => [message.data, ...prev].slice(0, 100));
        
        // Play alert sound for HIGH severity
        if (message.data.severity === 'HIGH') {
          playAlertSound();
        }
        
        // Show browser notification for HIGH alerts
        if (message.data.severity === 'HIGH' && 'Notification' in window) {
          if (Notification.permission === 'granted') {
            new Notification('🚨 HIGH Security Alert', {
              body: `${message.data.threat_type} detected`,
              icon: '/favicon.ico'
            });
          }
        }
      } else if (message.type === 'statistics') {
        // Update statistics
        setStats(message.data);
      } else if (message.type === 'ip_blocked') {
        fetchBlockedIPs();
      } else if (message.type === 'heartbeat') {
        console.log('💓 Heartbeat received');
      } else if (message.type === 'connected') {
        console.log('🔗 Connected to Mini SIEM');
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      setWsConnected(false);
    };

    ws.onclose = () => {
      console.log('❌ WebSocket Disconnected');
      setWsConnected(false);
      
      // Reconnect after 3 seconds
      setTimeout(connectWebSocket, 3000);
    };
  };

  const fetchInitialData = async () => {
    try {
      // Fetch recent alerts
      const alertsRes = await fetch('http://localhost:8000/alerts?limit=50');
      const alertsData = await alertsRes.json();
      setAlerts(alertsData);

      // Fetch statistics
      const statsRes = await fetch('http://localhost:8000/alerts/stats');
      const statsData = await statsRes.json();
      setStats({
        total_alerts: statsData.total_alerts || 0,
        by_severity: statsData.by_severity || { HIGH: 0, MEDIUM: 0, LOW: 0 },
        threat_distribution: statsData.threat_distribution || [],
        blocked_ips: 0,
        active_connections: 0
      });

      // Fetch blocked IPs
      fetchBlockedIPs();

      // Fetch system status
      const statusRes = await fetch('http://localhost:8000/system/status');
      const statusData = await statusRes.json();
      setSystemStatus(statusData);
      
      // Request notification permission
      if ('Notification' in window && Notification.permission === 'default') {
        Notification.requestPermission();
      }
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  const fetchBlockedIPs = async () => {
    try {
      const res = await fetch('http://localhost:8000/security/blocked-ips');
      const data = await res.json();
      setBlockedIPs(data);
    } catch (error) {
      console.error('Error fetching blocked IPs:', error);
    }
  };

  const playAlertSound = () => {
    try {
      if (!audioContextRef.current) {
        audioContextRef.current = new (window.AudioContext || window.webkitAudioContext)();
      }
      
      const audioContext = audioContextRef.current;
      const oscillator = audioContext.createOscillator();
      const gainNode = audioContext.createGain();
      
      oscillator.connect(gainNode);
      gainNode.connect(audioContext.destination);
      
      oscillator.frequency.value = 800;
      oscillator.type = 'sine';
      
      gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
      gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);
      
      oscillator.start(audioContext.currentTime);
      oscillator.stop(audioContext.currentTime + 0.5);
    } catch (error) {
      console.error('Error playing sound:', error);
    }
  };

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'HIGH': return '#ff4444';
      case 'MEDIUM': return '#ffaa00';
      case 'LOW': return '#44ff44';
      default: return '#888';
    }
  };

  const getThreatIcon = (threatType) => {
    const icons = {
      phishing: '📧',
      brute_force: '🔐',
      dos: '🌐',
      probe: '🔍',
      malware: '🦠',
      normal_login: '✅',
      normal_traffic: '✅',
      legitimate_email: '✅',
      safe_file: '✅'
    };
    return icons[threatType] || '⚠️';
  };

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleString();
  };

  return (
    <div className="dashboard">
      {/* Header */}
      <header className="dashboard-header">
        <div className="header-left">
          <h1>🛡️ Security Risk Detection with Human Readable Alerts</h1>
          <div className="live-clock">{currentTime.toLocaleTimeString()}</div>
        </div>
        <div className="connection-status">
          <span className={`status-indicator ${wsConnected ? 'connected' : 'disconnected'}`}></span>
          <span className="status-text">{wsConnected ? 'LIVE' : 'Disconnected'}</span>
          {wsConnected && <span className="pulse-animation">●</span>}
        </div>
      </header>

      {/* Statistics Cards */}
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Alerts</h3>
          <div className="stat-value">{stats.total_alerts || 0}</div>
          <div className="stat-label">All Time</div>
        </div>
        <div className="stat-card high">
          <h3>High Severity</h3>
          <div className="stat-value">{stats.by_severity?.HIGH || 0}</div>
          <div className="stat-label">Critical Threats</div>
        </div>
        <div className="stat-card medium">
          <h3>Medium Severity</h3>
          <div className="stat-value">{stats.by_severity?.MEDIUM || 0}</div>
          <div className="stat-label">Moderate Threats</div>
        </div>
        <div className="stat-card low">
          <h3>Low Severity</h3>
          <div className="stat-value">{stats.by_severity?.LOW || 0}</div>
          <div className="stat-label">Minor Issues</div>
        </div>
        <div className="stat-card">
          <h3>Blocked IPs</h3>
          <div className="stat-value">{blockedIPs.length}</div>
          <div className="stat-label">Quarantined</div>
        </div>
        <div className="stat-card">
          <h3>Active Connections</h3>
          <div className="stat-value">{stats.active_connections || 0}</div>
          <div className="stat-label">WebSocket Clients</div>
        </div>
      </div>

      {/* Main Content */}
      <div className="main-content">
        {/* Alert Feed */}
        <div className="alert-feed">
          <h2>🚨 Real-Time Alert Feed</h2>
          <div className="alerts-container">
            {alerts.length === 0 ? (
              <div className="no-alerts">
                <div className="loading-spinner"></div>
                <p>Waiting for security events...</p>
              </div>
            ) : (
              alerts.map((alert, index) => (
                <div 
                  key={alert._id || index} 
                  className={`alert-card severity-${alert.severity?.toLowerCase()} ${index === 0 ? 'new-alert' : ''}`}
                >
                  <div className="alert-header">
                    <span className="threat-icon">{getThreatIcon(alert.threat_type)}</span>
                    <span className="threat-type">{alert.event_type || alert.threat_type?.toUpperCase()}</span>
                    <span 
                      className="severity-badge"
                      style={{ backgroundColor: getSeverityColor(alert.severity) }}
                    >
                      {alert.severity}
                    </span>
                    <span className="risk-score">Risk: {alert.risk_score}/100</span>
                    {alert.ml_confidence && (
                      <span className="ml-confidence">ML: {(alert.ml_confidence * 100).toFixed(0)}%</span>
                    )}
                  </div>
                  
                  <div className="alert-body">
                    <div className="alert-source-info">
                      {alert.source_ip && (
                        <div className="info-item">
                          <strong>Source IP:</strong> {alert.source_ip}
                        </div>
                      )}
                      {alert.country && (
                        <div className="info-item">
                          <strong>🌍 Location:</strong> {alert.country}
                        </div>
                      )}
                      {alert.details?.country && !alert.country && (
                        <div className="info-item">
                          <strong>🌍 Location:</strong> {alert.details.country}
                        </div>
                      )}
                      {alert.threat_intelligence?.country && (
                        <div className="info-item">
                          <strong>🌍 Country:</strong> {alert.threat_intelligence.country}
                          {alert.threat_intelligence.city && ` (${alert.threat_intelligence.city})`}
                        </div>
                      )}
                      {alert.target_user && (
                        <div className="info-item">
                          <strong>Target User:</strong> {alert.target_user}
                        </div>
                      )}
                      {alert.source_email && (
                        <div className="info-item">
                          <strong>From:</strong> {alert.source_email}
                        </div>
                      )}
                      {alert.file_name && (
                        <div className="info-item">
                          <strong>File:</strong> {alert.file_name}
                        </div>
                      )}
                      {alert.detected_by && (
                        <div className="info-item">
                          <strong>Detected By:</strong> {alert.detected_by} ({alert.detection_method})
                        </div>
                      )}
                    </div>
                    
                    {alert.risk_factors && alert.risk_factors.length > 0 && (
                      <div className="risk-factors">
                        <strong>Threat Indicators:</strong>
                        <ul>
                          {alert.risk_factors.map((factor, i) => (
                            <li key={i}>{factor}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                  
                  <div className="alert-footer">
                    <span className="timestamp">
                      {formatTimestamp(alert.timestamp)}
                    </span>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Sidebar */}
        <div className="sidebar">
          {/* Threat Distribution */}
          <div className="widget">
            <h3>📊 Threat Distribution</h3>
            <div className="threat-list">
              {stats.threat_distribution && stats.threat_distribution.length > 0 ? (
                stats.threat_distribution.map((threat, index) => (
                  <div key={index} className="threat-item">
                    <span className="threat-icon">{getThreatIcon(threat._id)}</span>
                    <span className="threat-name">{threat._id || 'Unknown'}</span>
                    <span className="threat-count">{threat.count}</span>
                  </div>
                ))
              ) : (
                <div className="no-data">No threats detected yet</div>
              )}
            </div>
          </div>

          {/* Blocked IPs */}
          <div className="widget">
            <h3>🚫 Blocked IP Addresses</h3>
            <div className="blocked-ips-list">
              {blockedIPs.length === 0 ? (
                <div className="no-data">No blocked IPs</div>
              ) : (
                blockedIPs.map((ip, index) => (
                  <div key={index} className="blocked-ip-item">
                    <div className="ip-address">{ip.ip_address}</div>
                    <div className="ip-reason">{ip.reason}</div>
                    <div className="ip-time">
                      {formatTimestamp(ip.blocked_at)}
                    </div>
                    <div className="ip-count">Violations: {ip.block_count}</div>
                  </div>
                ))
              )}
            </div>
          </div>

          {/* System Status */}
          <div className="widget">
            <h3>⚙️ System Status</h3>
            <div className="system-info">
              <div className="info-item">
                <span>Status:</span>
                <span className="status-ok">{systemStatus.status || 'Unknown'}</span>
              </div>
              <div className="info-item">
                <span>Mode:</span>
                <span className="status-ok">{systemStatus.mode || 'N/A'}</span>
              </div>
              <div className="info-item">
                <span>Event Generator:</span>
                <span className={systemStatus.event_generator_running ? 'status-ok' : 'status-error'}>
                  {systemStatus.event_generator_running ? 'Running' : 'Stopped'}
                </span>
              </div>
              <div className="info-item">
                <span>Last Update:</span>
                <span>{currentTime.toLocaleTimeString()}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
