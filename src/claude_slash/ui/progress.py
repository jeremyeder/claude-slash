"""
Progress and spinner management utilities for long-running operations.
"""

import time
from contextlib import contextmanager
from typing import Any, Generator, Optional, Callable

from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TimeElapsedColumn,
    MofNCompleteColumn,
    TransferSpeedColumn,
    FileSizeColumn,
)
from rich.status import Status

from .console import get_console


class ProgressManager:
    """
    Manager for Rich progress bars with predefined configurations.
    """
    
    @staticmethod
    def download_progress() -> Progress:
        """
        Create a progress bar optimized for download operations.
        
        Returns:
            Progress instance with download-specific columns
        """
        return Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            FileSizeColumn(),
            TransferSpeedColumn(),
            TimeElapsedColumn(),
            console=get_console()
        )
    
    @staticmethod
    def file_progress() -> Progress:
        """
        Create a progress bar optimized for file operations.
        
        Returns:
            Progress instance with file-specific columns
        """
        return Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            MofNCompleteColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=get_console()
        )
    
    @staticmethod
    def simple_progress() -> Progress:
        """
        Create a simple progress bar for general operations.
        
        Returns:
            Progress instance with basic columns
        """
        return Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=get_console()
        )


class SpinnerManager:
    """
    Manager for Rich spinners with predefined configurations.
    """
    
    @staticmethod
    @contextmanager
    def network_operation(
        text: str = "Network operation in progress..."
    ) -> Generator[Status, None, None]:
        """
        Context manager for network operations with appropriate spinner.
        
        Args:
            text: Status text to display
            
        Yields:
            Status instance for updating spinner text
        """
        with get_console().status(text, spinner="dots") as status:
            yield status
    
    @staticmethod
    @contextmanager 
    def file_operation(
        text: str = "File operation in progress..."
    ) -> Generator[Status, None, None]:
        """
        Context manager for file operations with appropriate spinner.
        
        Args:
            text: Status text to display
            
        Yields:
            Status instance for updating spinner text
        """
        with get_console().status(text, spinner="line") as status:
            yield status
    
    @staticmethod
    @contextmanager
    def git_operation(
        text: str = "Git operation in progress..."
    ) -> Generator[Status, None, None]:
        """
        Context manager for git operations with appropriate spinner.
        
        Args:
            text: Status text to display
            
        Yields:
            Status instance for updating spinner text
        """
        with get_console().status(text, spinner="arc") as status:
            yield status


@contextmanager
def track_operation(
    description: str,
    total: Optional[int] = None,
    operation_type: str = "simple"
) -> Generator[tuple, None, None]:
    """
    Context manager for tracking operations with appropriate progress display.
    
    Args:
        description: Description of the operation
        total: Total items to process (if known)
        operation_type: Type of operation (simple, download, file)
        
    Yields:
        Tuple of (progress, task_id) for updating progress
        
    Example:
        with track_operation("Processing files", total=100, operation_type="file") as (progress, task):
            for i in range(100):
                # Do work
                progress.update(task, advance=1)
    """
    progress_managers = {
        "simple": ProgressManager.simple_progress,
        "download": ProgressManager.download_progress,
        "file": ProgressManager.file_progress,
    }
    
    progress_func = progress_managers.get(operation_type, ProgressManager.simple_progress)
    
    with progress_func() as progress:
        task_id = progress.add_task(description, total=total)
        yield progress, task_id


def run_with_spinner(
    func: Callable[[], Any],
    text: str = "Working...",
    spinner_type: str = "dots"
) -> Any:
    """
    Run a function with a spinner displayed.
    
    Args:
        func: Function to execute
        text: Spinner text
        spinner_type: Type of spinner (dots, line, arc, etc.)
        
    Returns:
        Result of the function call
    """
    with get_console().status(text, spinner=spinner_type):
        return func()


def simulate_progress(
    description: str,
    total: int = 100,
    delay: float = 0.01
) -> None:
    """
    Simulate a progress operation for testing/demo purposes.
    
    Args:
        description: Progress description
        total: Total progress steps
        delay: Delay between steps in seconds
    """
    with ProgressManager.simple_progress() as progress:
        task = progress.add_task(description, total=total)
        for i in range(total):
            time.sleep(delay)
            progress.update(task, advance=1)