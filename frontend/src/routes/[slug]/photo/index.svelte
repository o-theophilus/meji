<script>
	import { module, app } from '$lib/store.svelte.js';

	import Edit_Button from '../edit_button.svelte';
	import Form from './form.svelte';

	let { item, edit_mode, update } = $props();
	let src = $derived(item.files[0] || '/no_photo.png');
</script>

<div class="img">
	<img {src} alt={item.name} onerror={() => (src = '/no_photo.png')} />
	<div class="edit">
		{#if app.user.access.includes('item:edit_file') && edit_mode}
			<Edit_Button
				onclick={() => {
					module.open(Form, {
						key: item.key,
						name: item.name,
						files: item.files,
						update
					});
				}}
			>
				Edit Files
			</Edit_Button>
		{/if}
	</div>
</div>

<!-- TODO: improve carousel -->
{#if item.files.length > 1}
	<div class="line">
		{#each item.files as x}
			<img
				src="{x}/200"
				alt={item.name}
				class:active={src == x}
				onclick={() => (src = x)}
				onerror={(e) => (e.target.src = '/no_photo.png')}
				role="presentation"
			/>
		{/each}
	</div>
{/if}

<style>
	.img {
		position: relative;
	}

	img {
		display: block;

		width: 100%;
		border-radius: 8px;

		background-color: var(--bg1);
	}
	.edit {
		position: absolute;
		bottom: 8px;
		left: 8px;
	}

	.line {
		--size: 50px;

		display: flex;
		justify-content: center;
		align-items: center;
		gap: 8px;
		flex-wrap: wrap;
		margin-top: 16px;
	}

	.line img {
		width: var(--size);
		height: var(--size);
		border-radius: 4px;
		cursor: pointer;

		background-color: var(--bg1);
		outline: 2px solid transparent;
		transition:
			outline-color 0.2s ease-in-out,
			transform 0.2s ease-in-out;
	}

	.line img:hover {
		outline-color: var(--cl1);
	}

	.line img.active {
		outline-color: var(--cl1);
		transform: scale(1.1);
	}
</style>
