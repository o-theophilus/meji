<script>
	import { app, page_state, module } from '$lib/store.svelte.js';

	import { Form } from '$lib/layout';
	import { Tag, RoundButton } from '$lib/button';
	import { IG } from '$lib/input';

	let filter = $state('');
</script>

<Form title="All Tags">
	<IG type="text" placeholder="filter" bind:value={filter} no_pad>
		{#snippet right()}
			{#if filter}
				<div class="close">
					<RoundButton --button-background-color-hover="red" icon="x" onclick={() => (filter = '')}
					></RoundButton>
				</div>
			{/if}
		{/snippet}
	</IG>

	<div class="tags_space">
		{#each app.tags as tag}
			{#if tag.toLowerCase().includes(filter.toLowerCase())}
				<Tag
					onclick={() => {
						page_state.goto('shop', { tag });
						module.close();
					}}
				>
					{tag}
				</Tag>
			{/if}
		{/each}
	</div>
</Form>

<style>
	.tags_space {
		display: flex;
		flex-wrap: wrap;
		gap: 4px;

		max-height: 200px;
		overflow-y: auto;
	}
	.close {
		margin-right: 8px;
	}
</style>
