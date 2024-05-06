<script>
	import Card from '$lib/card.svelte';

	let width;
</script>

<svelte:window bind:innerWidth={width} />

<Card>
	<div class="skeleton_frame">
		{#each Array(8).slice(0, width < 700 ? 2 : width < 1000 ? 3 : 4) as _}
			<div class="item" />
		{/each}
	</div>
</Card>

<style>
	.skeleton_frame {
		display: grid;
		gap: var(--sp2);
		grid-template-columns: repeat(2, 1fr);

		color: var(--ac1);
	}

	@media screen and (min-width: 700px) {
		.skeleton_frame {
			grid-template-columns: repeat(3, 1fr);
		}
	}

	@media screen and (min-width: 1000px) {
		.skeleton_frame {
			grid-template-columns: repeat(4, 1fr);
		}
	}

	.skeleton_frame .item {
		display: flex;
		justify-content: center;
		align-items: center;
		aspect-ratio: 1/1;

		width: 100%;
		border-radius: var(--sp1);

		animation: blink 2s infinite linear;
	}

	@keyframes blink {
		0% {
			background-color: var(--ac5);
		}
		50% {
			background-color: var(--ac6);
		}
		100% {
			background-color: var(--ac5);
		}
	}
</style>
