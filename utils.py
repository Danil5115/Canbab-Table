import matplotlib.pyplot as plt 
import matplotlib.dates as mdates
import os
from datetime import datetime

plt.switch_backend('Agg')

def calculate_burndown(tasks):
    burndown_data = {'To Do': 0, 'In Progress': 0, 'Done': 0}
    for task in tasks:
        burndown_data[task.status] += 1
    return burndown_data

def calculate_velocity(tasks):
    velocity_data = {}
    for task in tasks:
        if task.status == 'Done' and task.sprint:
            sprint_name = task.sprint.name
            if sprint_name not in velocity_data:
                velocity_data[sprint_name] = 0
            velocity_data[sprint_name] += 1
    return velocity_data

def calculate_lead_time(tasks):
    lead_times = []
    for task in tasks:
        if task.done_at: 
            lead_time = (task.done_at - task.created_at).total_seconds() / 3600
            lead_times.append(lead_time)
    return lead_times

def calculate_cycle_time(tasks):
    cycle_times = []
    for task in tasks:
        if task.done_at and task.in_progress_at: 
            cycle_time = (task.done_at - task.in_progress_at).total_seconds() / 3600
            cycle_times.append(cycle_time)
    return cycle_times

def calculate_time_in_process(tasks):
    time_in_process = {'To Do': [], 'In Progress': [], 'Done': []}
    for task in tasks:
        if task.in_progress_at:
            to_do_time = (task.in_progress_at - task.created_at).total_seconds() / 3600
            time_in_process['To Do'].append(to_do_time)
        if task.done_at:
            in_progress_time = (task.done_at - task.in_progress_at).total_seconds() / 3600
            time_in_process['In Progress'].append(in_progress_time)
    return time_in_process

def plot_burndown(data):
    if not any(data.values()):
        return
    plt.figure(figsize=(10, 5))
    statuses = list(data.keys())
    counts = list(data.values())
    plt.bar(statuses, counts, color=['#1f77b4', '#ff7f0e', '#2ca02c'])
    plt.title('Burndown Chart')
    plt.xlabel('Status')
    plt.ylabel('Number of Tasks')
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.gca().yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plt.savefig(os.path.join('static', 'burndown.png'))
    plt.close()

def plot_velocity(data):
    if not data:
        return
    plt.figure(figsize=(10, 5))
    labels = list(data.keys())
    values = list(data.values())
    plt.bar(labels, values, color='#1f77b4')
    plt.title('Velocity Chart')
    plt.xlabel('Sprints')
    plt.ylabel('Completed Tasks')
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.gca().yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plt.savefig(os.path.join('static', 'velocity.png'))
    plt.close()

def plot_lead_time_histogram(data):
    if not data:
        return
    plt.figure(figsize=(10, 5))
    plt.hist(data, bins=20, color='#1f77b4')
    plt.title('Lead Time (Histogram)')
    plt.xlabel('Hours')
    plt.ylabel('Number of Tasks')
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.gca().yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plt.savefig(os.path.join('static', 'lead_time_histogram.png'))
    plt.close()

def plot_lead_time_box(data):
    if not data:
        return
    plt.figure(figsize=(10, 5))
    plt.boxplot(data)
    plt.title('Lead Time (Box Plot)')
    plt.xlabel('Tasks')
    plt.ylabel('Hours')
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.gca().yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plt.savefig(os.path.join('static', 'lead_time_box.png'))
    plt.close()

def plot_cycle_time_box(data):
    if not data:
        return
    plt.figure(figsize=(10, 5))
    plt.boxplot(data)
    plt.title('Cycle Time (Box Plot)')
    plt.xlabel('Tasks')
    plt.ylabel('Hours')
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.gca().yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plt.savefig(os.path.join('static', 'cycle_time_box.png'))
    plt.close()

def plot_cycle_time_scatter(data):
    if not data:
        return
    plt.figure(figsize=(10, 5))
    plt.scatter(range(1, len(data) + 1), data)
    plt.title('Cycle Time (Scatter Plot)')
    plt.xlabel('Tasks')
    plt.ylabel('Hours')
    plt.xticks(range(1, len(data) + 1), fontsize=12)
    plt.yticks(fontsize=12)
    plt.gca().yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plt.savefig(os.path.join('static', 'cycle_time_scatter.png'))
    plt.close()

def plot_time_in_process_stacked(data):
    if not any(data.values()):
        return
    
    stages = ['To Do', 'In Progress']
    times = [data[stage] for stage in stages]
    
    max_length = max(len(times[0]), len(times[1]))
    for stage in stages:
        while len(data[stage]) < max_length:
            data[stage].append(0)
    
    total_times = [sum(x) for x in zip(*times)]
    
    plt.figure(figsize=(10, 5))
    bottom = [0] * max_length
    for stage in stages:
        plt.bar(range(1, max_length + 1), data[stage], bottom=bottom, label=stage)
        bottom = [bottom[i] + data[stage][i] for i in range(max_length)]
    
    plt.title('Time in Process (Stacked Bar Chart)')
    plt.xlabel('Tasks')
    plt.ylabel('Hours')
    plt.legend()
    plt.xticks(range(1, max_length + 1), fontsize=12)
    plt.yticks(fontsize=12)
    plt.gca().yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plt.savefig(os.path.join('static', 'time_in_process_stacked.png'))
    plt.close()

def plot_cumulative_flow(tasks):
    if not tasks:
        return
    times = [task.created_at for task in tasks] + \
            [task.in_progress_at for task in tasks if task.in_progress_at] + \
            [task.done_at for task in tasks if task.done_at]
    times = sorted(list(set(times)))

    if not times:
        return

    to_do_counts = []
    in_progress_counts = []
    done_counts = []

    for time in times:
        to_do_count = sum(1 for task in tasks if task.created_at <= time and (task.in_progress_at is None or task.in_progress_at > time))
        in_progress_count = sum(1 for task in tasks if task.in_progress_at and task.in_progress_at <= time and (task.done_at is None or task.done_at > time))
        done_count = sum(1 for task in tasks if task.done_at and task.done_at <= time)
        
        to_do_counts.append(to_do_count)
        in_progress_counts.append(in_progress_count)
        done_counts.append(done_count)
    
    plt.figure(figsize=(10, 5))
    plt.plot(times, to_do_counts, label='To Do')
    plt.plot(times, in_progress_counts, label='In Progress')
    plt.plot(times, done_counts, label='Done')
    plt.fill_between(times, to_do_counts, alpha=0.3)
    plt.fill_between(times, in_progress_counts, alpha=0.3)
    plt.fill_between(times, done_counts, alpha=0.3)
    plt.title('Cumulative Flow Diagram')
    plt.xlabel('Time')
    plt.ylabel('Number of Tasks')
    plt.legend()
    
    # Formatting date ticks
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45, ha='right')
    
    plt.yticks(fontsize=12)
    plt.gca().yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plt.tight_layout()  # Adjust layout to make room for the rotated labels
    plt.savefig(os.path.join('static', 'cumulative_flow.png'))
    plt.close()