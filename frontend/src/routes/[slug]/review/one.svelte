<script>
	import { onMount } from 'svelte';
	import { page } from '$app/state';
	import { Datetime, Avatar } from '$lib/macro';
	import { scroll } from '$lib/store.svelte.js';
	import Details from './one.details.svelte';

	let { review, control } = $props();

	// TODO: test this scroll
	onMount(() => {
		if (page.url.hash == `#${review.key}`) {
			scroll(`#${review.key}`);
		}
	});
</script>

<section id={review.key}>
	{#if review.parent_key}
		<div
			class="parent"
			onclick={() => {
				scroll(`#${review.parent_key}`);
			}}
			role="presentation"
		>
			<Details review={review.parent}></Details>
		</div>
	{/if}
	<div class="review">
		<Details {review}></Details>
	</div>
	{@render control?.()}
</section>

<style>
	section {
		margin-top: 8px;
		padding: var(--sp2);
		border-radius: 8px;
		background-color: var(--bg3);
	}
	.parent {
		border-radius: 8px;
		border: 2px solid var(--bg2);
		padding: 16px;
	}
	section:has(.parent) .review {
		padding-top: 16px;
	}
	.review {
		padding-bottom: 16px;
	}
</style>
