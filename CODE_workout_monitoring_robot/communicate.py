from PySide6.QtCore import Signal, QObject

class Communicate(QObject):
    hello_signal = Signal()
    dashboard_signal = Signal()
    monitor_signal = Signal()
    tutorial_signal = Signal()
    stop_monitoring_signal = Signal()