<script>
	import { Tag } from '$lib/button';
	import { Card } from '$lib/layout';
	import { Marked } from '$lib/macro';
	import { app, module } from '$lib/store.svelte.js';
	import Edit_Button from '../edit_button.svelte';
	import FormTag from '../tag/form.svelte';
	import FormInfo from './form.svelte';

	let { item, edit_mode, update } = $props();
	let open = $state(true);
	let edit_into = $derived(app.user.access.includes('item.edit_information') && edit_mode);
	let edit_tag = $derived(app.user.access.includes('item.edit_tag') && edit_mode);
</script>

{#if item.information || item.tags.length || edit_into}
	<div class="hr"></div>
	<Card
		{open}
		onclick={() => (open = !open)}
		--card-title-padding="0"
		--card-content-padding="16px 0"
	>
		{#snippet title()}
			<div class="line">
				{#if edit_into}
					<Edit_Button
						onclick={() =>
							module.open(FormInfo, {
								key: item.key,
								information: item.information,
								update
							})}>Edit information</Edit_Button
					>
				{/if}
				{#if edit_tag}
					<Edit_Button
						onclick={() =>
							module.open(FormTag, {
								key: item.key,
								name: item.name,
								tags: item.tags,
								update
							})}
						>Edit Tags
					</Edit_Button>
				{/if}
			</div>
			<div class="title">Details & Specifications</div>
		{/snippet}

		{#if item.tags.length}
			<div class="line">
				{#each item.tags as x}
					<Tag onclick={() => page_state.goto('shop', { tag: x })}>
						{x}
					</Tag>
				{/each}
			</div>
		{:else if edit_tag}
			No tag
		{/if}

		{#if item.information}
			<Marked content={item.information}></Marked>
		{:else if edit_into}
			<div class="null">No information</div>
		{/if}
	</Card>
{/if}

<style>
	.hr {
		margin-top: 16px;
		background-color: var(--ft1);
		height: 1px;
	}

	.title {
		display: flex;
		align-items: center;
		gap: 16px;

		font-weight: 800;
		color: var(--ft1);
	}

	.null {
		margin-top: 16px;
	}
</style>
