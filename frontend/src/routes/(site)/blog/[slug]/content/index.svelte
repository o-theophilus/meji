<script>
	import { app, module } from '$lib/store.svelte.js';

	import { PageNote } from '$lib/info';
	import { Marked } from '$lib/macro';
	import Button from '../button.svelte';
	import Edit from './edit.svelte';
	import File from './file.svelte';

	let { blog, edit_mode, update } = $props();

	const process = (x) => {
		let temp = x.content;
		if (!temp) return '';

		let exist = temp.search(/@\[file\]/) >= 0;
		let i = 0;

		while (exist) {
			let sub = `![${x.title}](/no_file.png)`;
			if (x.files[i]) {
				if (x.files[i].slice(-4) == '.jpg') {
					sub = `![${x.title}](${x.files[i]})`;
				}
			}

			temp = temp.replace(/@\[file\]/, sub);
			exist = temp.search(/@\[file\]/) >= 0;
			i++;
		}
		return temp;
	};
</script>

<div class="area" class:edit={edit_mode}>
	{#if edit_mode}
		<div class="line">
			{#if app.user.access.includes('blog.edit_content')}
				<Button onclick={() => module.open(Edit, { blog, update, process })}>Edit Content</Button>
			{/if}

			{#if app.user.access.includes('blog.edit_files') && blog.content && blog.content.includes('@[file]')}
				<Button icon="image" onclick={() => module.open(File, { blog, update })}
					>Manage Files</Button
				>
			{/if}
		</div>
	{/if}

	{#if blog.content}
		<br />
		<Marked content={process(blog)} />
	{:else}
		<PageNote>No content</PageNote>
	{/if}
</div>

<style>
	.area {
		margin-top: 16px;
		border-top: 1px solid var(--ft1);

		&.edit {
			padding: 8px;
			border-radius: 4px;
			outline: 1px solid var(--ol);
			outline-offset: -1px;
		}
	}
</style>
