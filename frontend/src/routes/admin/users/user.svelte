<script>
	import Button from '$lib/button.svelte';

	export let user;
</script>

<section>
	<img src={user.photo || '/image/user.png'} alt={user.name} />
	<div class="right">
		<div class="name">
			{user.name}
		</div>

		Email:<span> {user.email} </span>

		<br />

		<Button class="link" href="/profile?search={user.key}">View</Button>
	</div>
</section>

<style>
	section {
		display: flex;
		gap: var(--sp2);
		padding: var(--sp2) 0;
		border-bottom: 1px solid var(--ac4);
		color: var(--ac2);
	}

	img {
		--size: 40px;
		width: var(--size);
		height: var(--size);

		border-radius: 50%;
	}

	.right {
		width: 100%;
	}
	span {
		word-wrap: break-word;
		word-break: break-all;
	}

	.name {
		font-weight: 500;
		color: var(--ac1);
	}
</style>
