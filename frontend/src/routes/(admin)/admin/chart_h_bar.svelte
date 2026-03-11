<script>
	import { onMount } from 'svelte';

	let { data = [] } = $props();
	let canvas;

	onMount(() => {
		const labels = data.map((x) => x.status);
		const counts = data.map((x) => x.count);

		new Chart(canvas, {
			type: 'bar',
			data: {
				labels: labels,
				datasets: [
					{
						label: 'Orders',
						data: counts,
						backgroundColor: ['#94a3b8', '#3b82f6', '#f59e0b', '#22c55e', '#ef4444']
					}
				]
			},
			options: {
				indexAxis: 'y',
				responsive: true,
				plugins: {
					legend: { display: false }
				},
				scales: {
					x: {
						beginAtZero: true,
						ticks: {
							precision: 0, // ensures integers, no decimals,
							// stepSize: 1
						}
					}
				}
			}
		});
	});
</script>

<canvas bind:this={canvas}></canvas>
