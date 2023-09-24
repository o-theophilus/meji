<script>
	import { onMount } from 'svelte';
	import { module } from '$lib/store.js';

	import Card from '$lib/card.svelte';
	import SVG from '$lib/svg.svelte';
	import Button from '$lib/button.svelte';

	import Tag from './tag.svelte';
	import Tags from './_tags.svelte';

	let tags = [];

	onMount(async () => {
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/tags`);
		resp = await resp.json();

		if (resp.status == 200) {
			tags = resp.tags;
		}
	});
</script>

{#if tags.length > 0}
	<div id="tag" />
	<Card>
		<div class="title">
			Tags
			<Button
				class="link"
				on:click={() => {
					$module = {
						module: Tags,
						tags
					};
				}}
			>
				view all <SVG type="arrow_right" size="16" />
			</Button>
		</div>

		<div class="item_area">
			{#each tags.slice(0, 6) as tag}
				<Tag {tag} />
			{/each}
		</div>
	</Card>
{/if}

<style>
	.title {
		font-weight: 600;
		display: flex;
		justify-content: space-between;
	}
	.title {
		fill: currentColor;
	}
</style>
