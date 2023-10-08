<script>
	import { module } from '$lib/store.js';

	import Card from '$lib/card.svelte';
	import SVG from '$lib/svg.svelte';
	import Button from '$lib/button.svelte';

	import Tag from './tag.svelte';
	import Tags from './_tags.svelte';

	export let tags = [];
	let width;
</script>

<svelte:window bind:innerWidth={width} />

{#if tags.length > 0}
	<div id="tag" />
	<Card>
		<div class="ctitle">Tags</div>

		<br />
		<br />

		<div class="item_area">
			{#each tags.slice(0, width < 1000 ? 6 : 8) as tag}
				<Tag {tag} />
			{/each}
		</div>
		<br />
		<Button
			class="wide"
			on:click={() => {
				$module = {
					module: Tags,
					tags
				};
			}}
		>
			View All

			<span class="rotate">
				<SVG type="angle" size="10" />
			</span>
		</Button>
	</Card>
{/if}

<style>
	.rotate {
		transform: rotate(180deg);
	}
</style>
