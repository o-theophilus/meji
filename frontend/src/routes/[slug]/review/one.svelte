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
	<div class="review">
		<Details {review}></Details>
	</div>

	{@render control?.()}

	{#each review.replies as reply}
		<div class="reply">
			<Details review={reply} admin></Details>
		</div>
	{/each}
</section>

<style>
	section {
		margin-top: 8px;
		padding: var(--sp2);
		border-radius: 8px;
		background-color: var(--bg3);
	}
	.review {
		padding-bottom: 16px;
	}
	.reply {
		border-top: 1px solid var(--bg2);
		margin-top: 16px;
		padding-top: 16px;
	}
</style>
