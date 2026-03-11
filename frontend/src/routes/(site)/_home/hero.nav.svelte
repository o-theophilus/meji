<script>
	import { page } from '$app/state';
	import { scroll } from '$lib/store.svelte.js';
</script>

<section>
	{#if page.data.new_arrivals?.length > 0}
		<button onclick={() => scroll('#new_arrivals')}> New Arrivals </button>
	{/if}
	{#if page.data.discount?.length > 0}
		<button onclick={() => scroll('#discount')}> Discount </button>
	{/if}
	<button onclick={() => scroll('#about')}> About Us </button>
	<button onclick={() => scroll('contact')}> Contact </button>
</section>

<style>
	section {
		display: flex;
		flex-wrap: wrap;
		justify-content: center;
		gap: 4px 16px;

		padding: 24px;
		padding-top: calc(24px * 2);

		font-size: 0.8rem;
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
