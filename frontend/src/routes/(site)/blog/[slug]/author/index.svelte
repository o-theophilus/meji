<script>
	import { app, module } from '$lib/store.svelte.js';

	import { Spinner, User } from '$lib/macro';
	import Button from '../button.svelte';
	import Form from './edit.svelte';

	let { author, blog, edit_mode, loading, update } = $props();
	let edit = $derived(app.user.access.includes('blog.edit_author') && edit_mode);
</script>

{#if loading || author.username}
	<div class="area" class:edit>
		{#if edit}
			<Button onclick={() => module.open(Form, { key: blog.key, update })}>Edit Author</Button>
		{/if}

		{#if loading}
			<div class="line">
				<Spinner active={loading} size="20" />
			</div>
		{:else}
			<User user={author}>(Author)</User>
		{/if}
	</div>
{/if}

<style>
	.area {
		margin-top: 32px;
		border-top: 1px solid var(--ft1);
		padding-top: 16px;
		&.edit {
			padding: 8px;
			border-radius: 4px;
			outline: 1px solid var(--ol);
			outline-offset: -1px;
		}
	}

	.line {
		gap: 16px;
	}
</style>
