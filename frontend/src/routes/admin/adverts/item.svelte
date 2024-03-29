<script>
	export let advert;
	export let sizes;

	let missing = '';
	for (let x of sizes) {
		if (!advert[`photo_${x}`]) {
			missing = missing ? `${missing}, ${x}` : x;
		}
	}
</script>

<a href="/admin/adverts/{advert.key}">
	<img src={advert.photo || '/image/item.png'} alt={advert.name} />
	<div class="details">
		<div class="name">
			{advert.name}
		</div>
		{#if advert.spaces.length > 0}
			Spaces:
			{#each advert.spaces as x, i}
				{#if i > 0} , {/if}
				{x}
			{/each}
		{/if}
		{#if missing}
			<br />
			<span class="error">
				missing:
				{missing}
			</span>
		{/if}
	</div>
</a>

<style>
	a {
		display: flex;
		align-items: center;
		gap: var(--sp2);
		padding: var(--sp2) 0;
		border-bottom: 2px solid var(--ac5);

		text-decoration: none;
		color: var(--ac2);
	}

	img {
		--size: 40px;
		width: var(--size);
		height: var(--size);

		border-radius: 50%;
	}

	.details {
		width: 100%;
	}

	.name {
		font-weight: 500;
		color: var(--ac1);
	}
</style>
