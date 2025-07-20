"""
Progress tracking and visualization utilities.

Provides progress bars and status updates for CLI.
"""

from typing import Optional, Callable, Any
import click
from click._termui_impl import ProgressBar
from datetime import datetime, timedelta
import threading
import time



class ProgressTracker:
    """
    Tracks processing progress with visual feedback.
    
    Features:
    - Progress bars with ETA
    - Item counters
    - Speed calculations
    - Error tracking
    """
    
    def __init__(self, 
                 total_items: int,
                 label: str = "Processing",
                 show_eta: bool = True,
                 show_speed: bool = True):
        """
        Initialize progress tracker.
        
        Args:
            total_items: Total number of items to process
            label: Progress bar label
            show_eta: Show estimated time remaining
            show_speed: Show processing speed
        """
        self.total_items = total_items
        self.label = label
        self.show_eta = show_eta
        self.show_speed = show_speed
        
        self.processed = 0
        self.failed = 0
        self.start_time: datetime | None = None
        self.progress_bar: ProgressBar[int] | None = None
        
    def start(self) -> None:
        """Start progress tracking."""
        self.start_time = datetime.now()
        self.progress_bar = click.progressbar(
            length=self.total_items,
            label=self.label,
            show_eta=self.show_eta,
            show_percent=True,
            show_pos=True
        )
        self.progress_bar.__enter__()
        
    def update(self, success: bool = True) -> None:
        """
        Update progress.
        
        Args:
            success: Whether the item was processed successfully
        """
        if success:
            self.processed += 1
        else:
            self.failed += 1
        
        if self.progress_bar:
            self.progress_bar.update(1)
    
    def finish(self) -> None:
        """Finish progress tracking and show summary."""
        if self.progress_bar:
            self.progress_bar.__exit__(None, None, None)
        
        if self.start_time:
            elapsed = datetime.now() - self.start_time
            self._show_summary(elapsed)
    
    def _show_summary(self, elapsed: timedelta) -> None:
        """Show processing summary."""
        click.echo("\n" + "=" * 50)
        click.echo(f"Processing Complete")
        click.echo(f"Total items: {self.total_items}")
        click.echo(f"Processed: {self.processed}")
        
        if self.failed > 0:
            click.echo(f"Failed: {click.style(str(self.failed), fg='red')}")
        
        click.echo(f"Time elapsed: {elapsed}")
        
        if self.processed > 0 and elapsed.total_seconds() > 0:
            speed = self.processed / elapsed.total_seconds()
            click.echo(f"Average speed: {speed:.2f} items/second")


class SpinnerProgress:
    """
    Shows a spinner for indeterminate progress.
    
    Useful for operations without known duration.
    """
    
    def __init__(self, message: str = "Processing"):
        """
        Initialize spinner.
        
        Args:
            message: Message to display
        """
        self.message = message
        self.spinner_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        self.running = False
        self.thread: threading.Thread | None = None
        
    def start(self) -> None:
        """Start the spinner."""
        self.running = True
        self.thread = threading.Thread(target=self._spin)
        self.thread.start()
        
    def _spin(self) -> None:
        """Spinner animation loop."""
        i = 0
        while self.running:
            char = self.spinner_chars[i % len(self.spinner_chars)]
            click.echo(f'\r{char} {self.message}', nl=False)
            time.sleep(0.1)
            i += 1
            
    def stop(self, final_message: Optional[str] = None) -> None:
        """
        Stop the spinner.
        
        Args:
            final_message: Optional message to display after stopping
        """
        self.running = False
        if self.thread:
            self.thread.join()
        
        click.echo('\r' + ' ' * (len(self.message) + 3), nl=False)
        click.echo(f'\r{final_message or self.message}')


class BatchProgressTracker:
    """
    Tracks progress for batch operations.
    
    Shows progress for both batches and items within batches.
    """
    
    def __init__(self, 
                 total_batches: int,
                 items_per_batch: int):
        """
        Initialize batch tracker.
        
        Args:
            total_batches: Total number of batches
            items_per_batch: Items in each batch
        """
        self.total_batches = total_batches
        self.items_per_batch = items_per_batch
        self.current_batch = 0
        self.batch_bar: ProgressBar[int] | None = None
        self.item_bar: ProgressBar[int] | None = None
        
    def start(self) -> None:
        """Start batch tracking."""
        self.batch_bar = click.progressbar(
            length=self.total_batches,
            label="Batches",
            show_eta=True
        )
        self.batch_bar.__enter__()
        
    def start_batch(self, batch_num: int, batch_size: int) -> None:
        """
        Start tracking a new batch.
        
        Args:
            batch_num: Batch number
            batch_size: Number of items in this batch
        """
        self.current_batch = batch_num
        
        if self.item_bar:
            self.item_bar.__exit__(None, None, None)
            
        self.item_bar = click.progressbar(
            length=batch_size,
            label=f"  Batch {batch_num + 1}",
            show_eta=False
        )
        self.item_bar.__enter__()
        
    def update_item(self) -> None:
        """Update item progress within current batch."""
        if self.item_bar:
            self.item_bar.update(1)
            
    def finish_batch(self) -> None:
        """Finish current batch."""
        if self.item_bar:
            self.item_bar.__exit__(None, None, None)
            self.item_bar = None
            
        if self.batch_bar:
            self.batch_bar.update(1)
            
    def finish(self) -> None:
        """Finish all tracking."""
        if self.item_bar:
            self.item_bar.__exit__(None, None, None)
        if self.batch_bar:
            self.batch_bar.__exit__(None, None, None)


def format_size(size_bytes: float) -> str:
    """
    Format byte size as human-readable string.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


def format_duration(seconds: float) -> str:
    """
    Format duration as human-readable string.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted string (e.g., "2h 15m")
    """
    if seconds < 60:
        return f"{seconds:.0f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        minutes = (seconds % 3600) / 60
        return f"{hours:.0f}h {minutes:.0f}m"
