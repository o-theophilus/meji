<script>
	import { scale } from 'svelte/transition';
	import { backInOut } from 'svelte/easing';

	import Button from '$lib/comp/button.svelte';

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
		<div transition:scale|local={{ delay: 0, duration: 200, easing: backInOut }}>
			<Button
				icon="angle"
				on:click={() => {
					go('top');
				}}
			/>
		</div>
	</section>
{/if}

<style>
	section {
		position: sticky;
		bottom: var(--headerHeight);

		padding: var(--gap2);

		display: flex;
		justify-content: flex-end;
	}

	div {
		transform: rotate(90deg);
	}
</style>