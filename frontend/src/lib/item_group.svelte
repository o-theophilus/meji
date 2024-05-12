<script>
	import Title from '$lib/title.svelte';
	import Center from '$lib/center.svelte';
	import ItemPack from '$lib/item_pack.svelte';
	import Item from '$lib/item/index.svelte';
	import Link from '$lib/button/link.svelte';
	import ButtonFold from '$lib/button/fold.svelte';

	export let name = 'Group Name';
	export let items = [];
	export let style = 'grid';
	export let href = '';
	export let fold = false;
	export let open = true;
	const set_open = () => {
		open = !open;
	};

	let width;
</script>

<svelte:window bind:innerWidth={width} />
{#if items.length > 0}
	<div id={name.toLowerCase().replace(/ /g, '_')} />
	<Center>
		<div class="block">
			<Title>
				<div
					on:click={() => {
						if (fold) {
							set_open();
						}
					}}
					role="presentation"
					class:fold
				>
					{name}
				</div>

				<svelte:fragment slot="down">
					{#if href}
						<Link {href} icon>view more</Link>
					{/if}
				</svelte:fragment>

				<svelte:fragment slot="right">
					{#if fold}
						<ButtonFold {open} on:click={set_open} />
					{/if}
				</svelte:fragment>
			</Title>
			{#if open}
				<ItemPack let:style {style}>
					{#each items.slice(0, width < 1000 ? 6 : 8) as x (x.key)}
						<Item item={x} {style} />
					{/each}
				</ItemPack>
			{/if}
		</div>
	</Center>
{/if}

<style>
	.block {
		border-top: 2px solid var(--ac4);
	}

	.fold {
		cursor: pointer;
	}
</style>
