<script>
	import { user, module } from '$lib/store.js';

	import Card from '$lib/card.svelte';
	import Body from '$lib/comp/card_body.svelte';
	import Button from '$lib/button.svelte';

	import Photo from './_photo.svelte';
	import AddPhoto from './_photo_add.svelte';

	export let item;
	let index = 0;
</script>

<div class="img">
	<img src={item.photos.length > 0 ? item.photos[index] : '/image/item.png'} alt={item.name} />
	{#if $user && $user.roles.includes('admin')}
		<div class="h edit">
			<Button
				icon={item.photos.length == 0 ? 'add' : 'edit'}
				icon_size="12"
				class="tiny"
				on:click={() => {
					let _module = Photo;
					if (item.photos.length == 0) {
						_module = AddPhoto;
					}
					$module = {
						module: _module,
						data: {
							item
						}
					};
				}}
				tooltip="{item.photos.length == 0 ? 'Add' : 'Edit'} Photo"
			/>
			<Button icon="logo" icon_size="12" class="tiny" href="/{item.alias}/ads" tooltip="Ads" />
		</div>
	{/if}
</div>

{#if item.photos.length > 1}
	<div class="slide">
		{#each item.photos as photo, i}
			<button
				on:click={() => {
					index = i;
				}}
			>
				<img src={photo} alt={item.name} />
			</button>
		{/each}
	</div>
{/if}

<style>
	.img {
		position: relative;
		height: auto;
	}
	img {
		border-radius: var(--brad1);
		width: 100%;
	}
	.edit {
		position: absolute;
		bottom: var(--sp2);
		right: var(--sp2);
	}

	.slide {
		display: flex;
		justify-content: center;
		gap: var(--sp1);
		flex-wrap: wrap;
	}
	.slide button {
		border: none;
		background-color: transparent;
	}
	.slide img {
		--size: 50px;
		width: var(--size);
		height: var(--size);
		cursor: pointer;

		border: 2px solid var(--ac5);
		border-radius: var(--brad1);
		object-fit: cover;

		transition: var(--trans1);
	}
	.slide img:hover {
		border-color: var(--midtone);
		transform: scale(1.1);
	}
</style>
