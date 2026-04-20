<script>
	import { LinkArrow } from '$lib/button';
	import { faqs } from '../faq/faq';
	import Group from '../faq/group.svelte';

	let ops = $state({ open: null });
</script>

<div class="margin">
	<div class="title">FAQ</div>
	{#each faqs as x}
		{#if x.category == 'Orders & Shipping'}
			<Group bind:ops category={x}></Group>
		{/if}
	{/each}

	<br />

	<LinkArrow href="/faq">View More</LinkArrow>
</div>

<style>
	.margin {
		margin: 160px 0;
	}

	.title {
		font-size: 2rem;
		color: var(--ft1);
		line-height: 120%;
		font-weight: 600;
	}
</style>
