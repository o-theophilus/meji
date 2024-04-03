<script>
	import { goto } from '$app/navigation';
	import { module, loading } from '$lib/store.js';

	import Form from '$lib/form.svelte';
	import Button from '$lib/button.svelte';
	import Tag from '$lib/button.tag.svelte';
	import SVG from '$lib/svg_tags.svelte';

	let { tags } = $module;
</script>

<Form>
	<svelte:fragment slot="title">
		<b>Tags</b>
	</svelte:fragment>

	<div class="tags_space">
		{#each tags as tag}
			<Tag
				on:click={() => {
					$loading = 'loading . . .';
					$module = '';
					goto(`/shop?${new URLSearchParams({ tag }).toString()}`);
				}}
			>
				{tag}
			</Tag>
		{/each}
	</div>
</Form>

<style>
	.tags_space {
		display: flex;
		flex-wrap: wrap;
		gap: var(--sp1);

		max-height: 200px;
		overflow-y: auto;

		border-radius: var(--sp1);
		padding: var(--sp1);
		border: 2px solid var(--ac4);
	}
</style>
