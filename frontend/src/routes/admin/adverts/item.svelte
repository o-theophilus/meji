<script>
	export let advert;
</script>

<a href="/admin/adverts/{advert.key}">
	<img src={advert.item.photo || '/image/item.png'} alt={advert.item.name} />
	<div class="details">
		<div class="name">
			{advert.item.name}
		</div>
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
		color: var(--ac1);
		font-weight: 500;
	}
</style>
