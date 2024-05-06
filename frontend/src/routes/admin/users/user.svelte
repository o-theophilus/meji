<script>
	export let user;
</script>

<a href="/profile?search={user.key}">
	<img src={user.photo || '/image/user.png'} alt={user.name} />
	<div class="details">
		<div class="name">
			{user.name}
		</div>

		<span>
			{user.email}
		</span>
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

		border-radius: 50%;
	}

	.details {
		width: 100%;
	}

	.name {
		font-weight: 700;
		color: var(--ac1);
	}

	span {
		word-wrap: break-word;
		word-break: break-all;
	}
</style>
