# Operating Systems Simulator

A Python-based operating systems simulation project completed through a series of five cumulative assignments in an Operating Systems course.

The project uses an **instructor-provided simulation framework** that models operating system components such as CPUs, interrupts, memory, devices, files, and processes. Across five assignments, I implemented core operating system functionality involving task management, CPU scheduling, virtual memory, file I/O, and disk scheduling.

## My Implementations

My work focused on five primary modules:

### Task Management — `Tasks.py`

Implemented task-management functionality including:

- Task creation and termination
- Task state management
- Thread ownership and tracking
- Open-file tracking
- Page-table initialization
- Swap-file creation and cleanup
- Resource cleanup when terminating tasks
- Task-related interrupt handling

### Thread Management & CPU Scheduling — `Threads.py`

Implemented thread-management and CPU-scheduling functionality including:

- Thread creation and termination
- Ready-queue management
- Thread state transitions
- Sleep and wake behavior for I/O
- Priority-based scheduling
- Round-Robin time quantum handling
- Dynamic priority adjustment
- Timer-based preemption
- CPU rescheduling and dispatching

### Virtual Memory — `Memory.py`

Implemented memory-management functionality including:

- Page tables
- Logical-to-physical address translation
- Page-fault handling
- Physical frame management
- Page locking and reservation
- LRU page replacement
- Victim-page eviction
- Swap-in and swap-out operations
- Dirty-page handling
- Memory deallocation

### File I/O — `OpenFileDescriptor.py`

Implemented file and asynchronous I/O functionality including:

- File read operations
- File write operations
- I/O request creation
- Page locking during I/O
- Thread suspension during asynchronous operations
- Pending-I/O tracking
- File growth and block allocation
- Delayed file closing while I/O is outstanding
- File cleanup and deletion handling

### Disk Management — `Disks.py`

Implemented disk-management functionality including:

- Disk initialization and geometry calculations
- Disk interrupt handling
- I/O request queue management
- Disk block addressing
- Free-block allocation and release
- Starting and completing disk I/O
- SCAN disk scheduling
- Disk-head direction management

## Operating Systems Concepts

This project provided hands-on experience with:

- Processes and tasks
- Threads
- CPU scheduling
- Preemption
- Interrupt handling
- Process and thread states
- Virtual memory
- Paging
- Page faults
- Page replacement
- Swapping
- File systems
- Asynchronous I/O
- Device drivers
- Disk scheduling
- Resource management

## Technologies

- Python
- PyCharm

## Project Structure

The five modules containing my primary assignment implementations are:

```text
Tasks.py                 # Task and process management
Threads.py               # Thread management and CPU scheduling
Memory.py                # Virtual memory and paging
OpenFileDescriptor.py    # File and asynchronous I/O
Disks.py                 # Disk management and SCAN scheduling
```

Additional Python modules in this repository are part of the simulation framework required for the implemented components to interact and operate.

## Assignment Progression

The project was completed incrementally throughout the course:

```text
Assignment 1
    ↓
Task Management

Assignment 2
    ↓
Thread Management & CPU Scheduling

Assignment 3
    ↓
Virtual Memory & Paging

Assignment 4
    ↓
File I/O

Assignment 5
    ↓
Disk Management & Scheduling
```

Each assignment built upon functionality from previous assignments, resulting in multiple operating system subsystems interacting within the same simulation environment.

## Attribution

This repository originates from an academic Operating Systems project.

The underlying simulator architecture, supporting framework, function headers, and documentation were provided by the course instructor. My contributions consist of implementing the required functionality within the assignment modules identified above.

This repository is presented as a portfolio demonstration of my work with operating systems concepts and Python programming.
