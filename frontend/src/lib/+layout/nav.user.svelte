<script>
	import { app } from '$lib/store.svelte.js';
	import { Avatar } from '$lib/macro';
</script>

<a href="/@{app.user.username}">
	<Avatar name={app.user.name} photo={app.user.photo} size="32" --avatar-border-radius="50%" />
</a>
