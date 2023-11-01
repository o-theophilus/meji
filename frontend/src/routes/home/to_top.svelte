<script>
	import { scale } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';

	import Button from '$lib/button.svelte';
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
			<Button
				class="round"
				on:click={() => {
					go('top');
				}}
			>
				<SVG type="angle" size="12" />
			</Button>
		</div>
	</section>
{/if}

<style>
	section {
		position: sticky;
		bottom: var(--headerHeight);

		padding: var(--sp2);
		padding-right: var(--sp4);

		display: flex;
		justify-content: flex-end;
	}

	div {
		transform: rotate(90deg);
	}
</style>
