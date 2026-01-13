<script>
	import { module } from '$lib/store.svelte.js';

	import { Link } from '$lib/button';

	import Tag from './tags.btn.svelte';
	import AllTags from './tags._all.svelte';

	let width;
	let tags = ['male', 'palm', 'female', 'sandals', 'sneakers', 'nike', 'timberland', 'cover shoe'];
</script>

<svelte:window bind:innerWidth={width} />

{#if tags.length > 0}
	<div id="tag"></div>
	Tags
	<Link
		on:click={() => {
			$module = {
				module: AllTags
			};
		}}
		icon
	>
		view more
	</Link>

	{#each tags.slice(0, width < 1000 ? 6 : 8) as tag}
		<Tag {tag} />
	{/each}
{/if}

<style>
</style>
