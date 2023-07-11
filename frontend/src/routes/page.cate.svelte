<script>
	import { goto } from '$app/navigation';
	// import { state } from '$lib/page_state.js';

	import SVG from '$lib/comp/svg2.svelte';

	export let category = {};
</script>

<button
	on:click={() => {
		// $state['shop'].search = '';
		// $state['shop'].category = cate.name;
		// $state['shop'].page_no = 1;
		goto('/shop');
	}}
>
	<SVG type={category.icon} size="30" />
	<div>
		{category.name}
	</div>
</button>

<style>
	button {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		gap: var(--sp1);

		height: 100px;
		width: 100%;
		padding: var(--sp2);
		border: 2px solid var(--ac4);

		color: var(--ac2);
		fill: var(--ac2);
		background-color: transparent;
		border-radius: var(--brad1);
		cursor: pointer;
		text-align: center;
		text-transform: capitalize;
	}
	button:hover {
		color: var(--ac1);
		fill: var(--ac1);
		border-color: var(--cl1);
	}

	@media screen and (min-width: 600px) {
		button {
			height: 150px;
		}
	}
</style>
