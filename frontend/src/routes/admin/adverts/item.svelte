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
	<div class="right">
		<div class="first_line">
			<span class="name">
				{advert.name}
			</span>
			<span class="status">
				{advert.status}
			</span>
		</div>
		<div class="other_line">
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
	</div>
</a>

<style>
	a {
		display: flex;
		align-items: center;
		gap: var(--sp2);

		margin-top: var(--sp2);
		padding-top: var(--sp2);
		border-top: 2px solid var(--ac5);

		text-decoration: none;
		color: var(--ac2);
	}

	img {
		--size: 40px;
		width: var(--size);
		height: var(--size);
		flex-shrink: 0;

		border-radius: 50%;
	}

	.right {
		width: 100%;
	}

	.first_line {
		display: flex;
		gap: var(--sp1);
		justify-content: space-between;
	}

	.name {
		font-weight: 700;
		color: var(--ac1);
	}

	.other_line,
	.status {
		font-size: small;
	}
</style>
