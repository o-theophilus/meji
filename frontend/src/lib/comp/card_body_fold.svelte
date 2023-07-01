<script>
	import { slide } from 'svelte/transition';
	import { elasticInOut } from 'svelte/easing';
</script>

<section transition:slide|local={{ delay: 0, duration: 200, easing: elasticInOut }}>
	<slot>No Item</slot>
</section>

<style>
	section {
		display: flex;
		flex-direction: column;
		gap: var(--gap2);

		width: 100%;

		color: var(--font1);

		padding: var(--gap2);
		/* border-top: 2px solid var(--background); */
	}
</style>
