<script>
	import { onMount } from 'svelte';
	import { page } from '$app/state';
	// import { state } from '$lib/store.js';

	const go = (name) => {
		document.querySelector(`#${name}`).scrollIntoView({
			behavior: 'smooth'
		});
	};

	// let tags = false;
	// onMount(async () => {
	// 	let i = $state.findIndex((x) => x.name == 'tags');
	// 	if (i != -1) {
	// 		tags = $state[i].data.length > 0;
	// 	}
	// });
</script>

<section>
	<button
		on:click={() => {
			go('top');
		}}
	>
		Home
	</button>

	<!-- {#if tags}
		<button
			on:click={() => {
				go('tag');
			}}
		>
			Tags
		</button>
	{/if} -->

	{#if page.data.new_arrivals?.length > 0}
		<button
			on:click={() => {
				go('new_arrivals');
			}}
		>
			New Arrivals
		</button>
	{/if}

	{#if page.data.offers?.length > 0}
		<button
			on:click={() => {
				go('offers');
			}}
		>
			Offers
		</button>
	{/if}

	<button
		on:click={() => {
			go('about');
		}}
	>
		About Us
	</button>

	<button
		on:click={() => {
			go('contact');
		}}
	>
		Contact
	</button>
</section>

<style>
	section {
		display: flex;
		flex-wrap: wrap;
		justify-content: center;
		gap: var(--sp2);

		padding: var(--sp3);
		padding-top: calc(var(--sp3) * 2);

		font-weight: 700;
		color: var(--ac2);
	}

	button {
		all: unset;
		cursor: pointer;
	}

	button:hover {
		color: var(--cl1);
	}
</style>
