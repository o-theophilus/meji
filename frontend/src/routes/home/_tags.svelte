<script>
	import { goto } from '$app/navigation';
	import { module, loading } from '$lib/store.js';

	import Form from '$lib/form.svelte';
	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg_tags.svelte';

	let { tags } = $module;
</script>

<Form>
	<svelte:fragment slot="title">
		<b>Tags</b>
	</svelte:fragment>

	<div class="tags">
		{#each tags as tag}
			<Button
				class="small"
				on:click={() => {
					$loading = "loading . . .";
					$module = '';
					goto(`/shop?${new URLSearchParams({ tag }).toString()}`);
				}}
			>
				<SVG type={tag} size="20" />
				{tag}
			</Button>
		{/each}
	</div>
</Form>

<style>
	.tags {
		display: flex;
		flex-wrap: wrap;
		gap: var(--sp1);
	}
</style>
