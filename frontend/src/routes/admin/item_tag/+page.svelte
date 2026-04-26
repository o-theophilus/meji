<script>
	import { Button, Tag } from '$lib/button';
	import { PageNote } from '$lib/info';
	import { Content } from '$lib/layout';
	import { Icon, Log, Meta } from '$lib/macro';
	import { app, module, page_state } from '$lib/store.svelte.js';

	import Delete from './form.delete.svelte';
	import Fearured from './form.featured.svelte';
	import Rename from './form.rename.svelte';
</script>

<Log entity_type={'page'} />
<Meta title="Manage Tags" />

<Content>
	<div class="page_title">Manage Tags</div>

	<div class="featured">
		<div class="title">
			Item Featured Tag{app.item_featured_tags.length > 1 ? 's' : ''}
		</div>

		{#if app.item_featured_tags.length}
			<div class="line tags">
				{#each app.item_featured_tags as x}
					<Tag onclick={() => page_state.goto('shop', { tag: x })}>
						{x}
					</Tag>
				{/each}
			</div>
		{:else}
			<PageNote>
				<Icon icon="tags" size="50" />
				No Featured Tag
			</PageNote>
		{/if}
		{#if app.user.access.includes('admin.tag.featured')}
			<Button icon="square-pen" onclick={() => module.open(Fearured)}>Edit Featured</Button>
		{/if}
	</div>
	<div class="line btns">
		{#if app.user.access.includes('admin.tag.rename')}
			<Button icon="square-pen" onclick={() => module.open(Rename)}>Rename tag</Button>
		{/if}
		{#if app.user.access.includes('admin.tag.delete')}
			<Button icon="trash-2" onclick={() => module.open(Delete)}>Delete tags</Button>
		{/if}
	</div>
</Content>

<style>
	.featured {
		margin-top: 24px;
		background-color: var(--bg);
		padding: 24px;
		border-radius: 8px;
	}

	.title {
		font-weight: 800;
	}

	.tags {
		margin: 24px 0;
		max-height: 280px;
		overflow: auto;
		outline: 1px solid var(--ol);
		border-radius: 8px;
		padding: 8px;
		outline-offset: -1px;
	}

	.btns {
		margin-top: 24px;
	}
</style>
