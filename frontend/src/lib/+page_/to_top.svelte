<script>
	import { scale } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';

	import BRound from '$lib/button/round.svelte';
	import SVG from '$lib/svg.svelte';

	const go = (name) => {
		document.querySelector(`#${name}`).scrollIntoView({
			behavior: 'smooth'
		});
	};

	let y;
</script>

<svelte:window bind:scrollY={y} />

{#if y > 500}
	<section>
		<div transition:scale|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
			<BRound
				extra="outline"
				on:click={() => {
					go('top');
				}}
			>
				<div class="svg">
					<SVG icon="angle" size="8" />
				</div>
			</BRound>
		</div>
	</section>
{/if}

<style>
	section {
		position: sticky;
		bottom: calc(var(--headerHeight) + var(--sp2));

		width: min(100%, 1200px);
		margin: var(--sp2) auto;
		padding: 0 var(--sp4);

		display: flex;
		justify-content: flex-end;
	}

	.svg {
		display: flex;
		justify-content: center;
		align-items: center;
		transform: rotate(90deg);
	}
</style>
