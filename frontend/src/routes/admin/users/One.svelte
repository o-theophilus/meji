<script>
	import { Avatar } from '$lib/macro';
	let { item } = $props();
</script>

<!-- TODO: indicate blocked user -->
<a href="/@{item.username}">
	<Avatar name={item.name} photo={item.photo} --avatar-border-radius="50%" />
	<div class="details">
		<div class="name">
			{item.name}
		</div>

		<span class="username">
			@{item.username}
		</span>
	</div>
</a>

<style>
	a {
		display: flex;
		align-items: center;
		gap: var(--sp2);

		margin-top: 8px;
		padding: 16px;
		background-color: var(--bg3);
		border-radius: 8px;

		text-decoration: none;
		color: var(--ft2);
		text-decoration: none;
		outline: 1px solid var(--ol);
		outline-offset: -1px;

		transition: background-color 0.2s ease-in-out;

		&:hover {
			background-color: var(--bg2);
		}

		& .details {
			width: 100%;
			line-height: 100%;
			& .name {
				font-weight: 700;
				color: var(--ft1);
			}
			& .username {
				font-size: 0.7em;
			}
		}
	}

	span {
		word-wrap: break-word;
		word-break: break-all;
	}
</style>
