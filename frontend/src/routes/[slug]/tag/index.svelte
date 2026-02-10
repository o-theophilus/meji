<script>
	import { Tag } from '$lib/button';
	import { app, module, page_state } from '$lib/store.svelte.js';
	import Edit_Button from '../edit_button.svelte';
	import Form from './form.svelte';

	let { item, edit_mode, update } = $props();
</script>

<!-- {#if item.tags.length > 0 || (app.user.access.includes('item:edit_tag') && edit_mode)}
	<hr />
{/if} -->

{#if app.user.access.includes('item:edit_tag') && edit_mode}
	<Edit_Button
		onclick={() =>
			module.open(Form, {
				key: item.key,
				name: item.name,
				tags: item.tags,
				update
			})}
		>Edit Tags
	</Edit_Button>
{/if}

{#if item.tags.length > 0}
	<div class="line">
		{#each item.tags as x}
			<Tag onclick={() => page_state.goto('shop', { tag: x })}>
				{x}
			</Tag>
		{/each}
	</div>
{:else if edit_mode}
	<div class="notag">No tag</div>
{/if}

<style>
	.notag {
		font-size: 0.8rem;
	}

	.line {
		margin-top: 8px;
		gap: 4px;
	}

	/* hr {
		margin: 16px 0;
	} */
</style>
